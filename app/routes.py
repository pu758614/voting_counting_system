import io
import json
from datetime import datetime
import pytz
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, make_response
from app import db
from app.models import Election, Candidate, VoteLog, taipei_tz, taipei_time
import xlsxwriter

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    elections = Election.query.order_by(Election.created_at.desc()).all()
    return render_template('index.html', elections=elections)

@main_bp.route('/election/new', methods=['GET', 'POST'])
def new_election():
    if request.method == 'POST':
        data = request.json

        election = Election(
            title=data['title'],
            total_voters=data['total_voters'],
            threshold_type=data['threshold_type'],
            threshold_value=data['threshold_value']
        )

        db.session.add(election)

        for candidate_name in data['candidates']:
            candidate = Candidate(name=candidate_name, election=election)
            db.session.add(candidate)

        db.session.commit()

        return jsonify({'success': True, 'election_id': election.id})

    return render_template('new_election.html')

@main_bp.route('/election/<int:election_id>')
def view_election(election_id):
    election = Election.query.get_or_404(election_id)
    candidates = Candidate.query.filter_by(election_id=election_id).all()
    vote_logs = VoteLog.query.filter_by(election_id=election_id).order_by(VoteLog.timestamp.desc()).all()

    return render_template('view_election.html', election=election, candidates=candidates, vote_logs=vote_logs)

@main_bp.route('/election/<int:election_id>/delete', methods=['POST'])
def delete_election(election_id):
    try:
        # First delete all vote logs associated with this election
        VoteLog.query.filter_by(election_id=election_id).delete()

        # Then delete all candidates
        Candidate.query.filter_by(election_id=election_id).delete()

        # Finally delete the election
        election = Election.query.get_or_404(election_id)
        db.session.delete(election)

        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@main_bp.route('/election/<int:election_id>/vote', methods=['POST'])
def vote(election_id):
    data = request.json
    candidate_id = data['candidate_id']
    vote_type = data['vote_type']  # '+' or '-'

    candidate = Candidate.query.get_or_404(candidate_id)
    election = Election.query.get_or_404(election_id)

    if vote_type == '+':
        candidate.votes += 1
    elif vote_type == '-':
        if candidate.votes > 0:
            candidate.votes -= 1

    vote_log = VoteLog(
        candidate_id=candidate_id,
        election_id=election_id,
        vote_type=vote_type
    )

    db.session.add(vote_log)

    # Check if this candidate has met the election threshold
    elected = False
    if election.threshold_type == 'percentage':
        required_votes = election.total_voters * election.threshold_value
        if candidate.votes >= required_votes:
            elected = True
            candidate.is_elected = True
    elif election.threshold_type == 'majority':
        if candidate.votes > election.total_voters / 2:
            elected = True
            candidate.is_elected = True

    db.session.commit()

    return jsonify({
        'success': True,
        'votes': candidate.votes,
        'elected': elected,
        'candidate_name': candidate.name
    })

@main_bp.route('/election/<int:election_id>/save', methods=['POST'])
def save_election(election_id):
    election = Election.query.get_or_404(election_id)
    election.is_completed = True
    db.session.commit()

    return jsonify({'success': True})

@main_bp.route('/election/<int:election_id>/export')
def export_election(election_id):
    election = Election.query.get_or_404(election_id)
    candidates = Candidate.query.filter_by(election_id=election_id).all()
    vote_logs = VoteLog.query.filter_by(election_id=election_id).order_by(VoteLog.timestamp).all()

    # Create an in-memory output file
    output = io.BytesIO()

    # Create a workbook and add a worksheet
    workbook = xlsxwriter.Workbook(output)

    # Formatting
    title_format = workbook.add_format({'bold': True, 'font_size': 14})
    header_format = workbook.add_format({'bold': True, 'bg_color': '#D9D9D9'})
    date_format = workbook.add_format({'num_format': 'yyyy-mm-dd hh:mm:ss'})

    # Results sheet
    results_sheet = workbook.add_worksheet("選舉結果")

    results_sheet.write(0, 0, election.title, title_format)
    results_sheet.write(1, 0, f"總選民數: {election.total_voters}")

    if election.threshold_type == 'percentage':
        threshold_text = f"當選條件: 獲得總選民數的 {int(election.threshold_value * 100)}%"
    else:
        threshold_text = "當選條件: 過半數"

    results_sheet.write(2, 0, threshold_text)

    # Write headers
    results_sheet.write(4, 0, "候選人", header_format)
    results_sheet.write(4, 1, "得票數", header_format)
    results_sheet.write(4, 2, "當選狀態", header_format)

    # Write candidate results
    for i, candidate in enumerate(candidates):
        row = 5 + i
        results_sheet.write(row, 0, candidate.name)
        results_sheet.write(row, 1, candidate.votes)
        results_sheet.write(row, 2, "當選" if candidate.is_elected else "")

    # Vote log sheet
    log_sheet = workbook.add_worksheet("投票紀錄")

    log_sheet.write(0, 0, "時間", header_format)
    log_sheet.write(0, 1, "候選人", header_format)
    log_sheet.write(0, 2, "投票", header_format)

    for i, log in enumerate(vote_logs):
        row = 1 + i
        log_sheet.write(row, 0, log.timestamp.strftime("%Y-%m-%d %H:%M:%S"))
        log_sheet.write(row, 1, log.candidate.name)
        log_sheet.write(row, 2, "+" if log.vote_type == "+" else "-")

    workbook.close()

    # Seek to the beginning of the stream
    output.seek(0)

    # Create a response
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename={election.title}_election_results.xlsx"
    response.headers["Content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    return response
from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

teams = Blueprint('teams', __name__)

@teams.route('/teams', methods=['GET', 'POST'])
def team():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new team
    if request.method == 'POST':
        name = request.form['name']
        conference = request.form['conference']
        location = request.form['location']

        # Insert the new team into the database
        cursor.execute(
            'INSERT INTO teams (name, conference, location) VALUES (%s, %s, %s)',
            (name, conference, location)
        )
        db.commit()

        flash('New team added successfully!', 'success')
        return redirect(url_for('teams.team'))

    # Handle GET request to display all teams
    cursor.execute('SELECT * FROM teams')
    all_teams = cursor.fetchall()
    return render_template('teams.html', all_teams=all_teams)

@teams.route('/update_team/<int:team_id>', methods=['GET', 'POST'])
def update_team(team_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Update the team's details
        name = request.form['name']
        conference = request.form['conference']
        location = request.form['location']

        cursor.execute(
            'UPDATE teams SET name = %s, conference = %s, location = %s WHERE team_id = %s',
            (name, conference, location, team_id)
        )
        db.commit()

        flash('Team updated successfully!', 'success')
        return redirect(url_for('teams.team'))

    # GET method: fetch team's current data for pre-populating the form
    cursor.execute('SELECT * FROM teams WHERE team_id = %s', (team_id,))
    current_team = cursor.fetchone()
    return render_template('update_team.html', current_team=current_team)

@teams.route('/delete_team/<int:team_id>', methods=['POST'])
def delete_team(team_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the team
    cursor.execute('DELETE FROM teams WHERE team_id = %s', (team_id,))
    db.commit()

    flash('Team deleted successfully!', 'danger')
    return redirect(url_for('teams.team'))

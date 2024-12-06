from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

players = Blueprint('players', __name__)

@players.route('/players', methods=['GET', 'POST'])
def player():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new player
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        high_school = request.form['high_school']
        recruitment_status = request.form['recruitment_status']

        # Insert the new player into the database
        cursor.execute(
            'INSERT INTO players (name, position, high_school, recruitment_status) VALUES (%s, %s, %s, %s)',
            (name, position, high_school, recruitment_status)
        )
        db.commit()

        flash('New player added successfully!', 'success')
        return redirect(url_for('players.player'))

    # Handle GET request to display all players
    cursor.execute('SELECT * FROM players')
    all_players = cursor.fetchall()
    return render_template('players.html', all_players=all_players)

@players.route('/update_player/<int:player_id>', methods=['GET', 'POST'])
def update_player(player_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        # Update the player's details
        name = request.form['name']
        position = request.form['position']
        high_school = request.form['high_school']
        recruitment_status = request.form['recruitment_status']

        cursor.execute(
            'UPDATE players SET name = %s, position = %s, high_school = %s, recruitment_status = %s WHERE player_id = %s',
            (name, position, high_school, recruitment_status, player_id)
        )
        db.commit()

        flash('Player updated successfully!', 'success')
        return redirect(url_for('players.player'))

    # GET method: fetch player's current data for pre-populating the form
    cursor.execute('SELECT * FROM players WHERE player_id = %s', (player_id,))
    current_player = cursor.fetchone()
    return render_template('update_player.html', current_player=current_player)

@players.route('/delete_player/<int:player_id>', methods=['POST'])
def delete_player(player_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the player
    cursor.execute('DELETE FROM players WHERE player_id = %s', (player_id,))
    db.commit()

    flash('Player deleted successfully!', 'danger')
    return redirect(url_for('players.player'))

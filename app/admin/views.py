from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_required

from . import admin
from .. import db
from ..models import Agency, User, Role
from .forms import AddAgencyForm, EditAgencyForm


@admin.route('/agency/add', methods=['GET', 'POST'])
# @login_required
def add_agency():
    form = AddAgencyForm()
    if form.validate_on_submit():
        agency = Agency(name=form.name.data,
                        address=form.address.data)
        db.session.add(agency)
        db.session.commit()
        flash('Agency {} was added to database.'.format(agency.name))
        return redirect(url_for('main.index'))
    return render_template("admin/add_agency.html", form=form)

@admin.route('/agency/detail/<int:agency_id>', methods=['GET', 'POST'])
@login_required
def detail_agency(agency_id):
    agency = Agency.query.get_or_404(agency_id)
    form = EditAgencyForm(obj=agency)
    if form.validate_on_submit():
        if form.update.data:
            form.populate_obj(agency)
            flash('Agency {} was updated successfully.'.format(agency.name))
        elif form.delete.data:
            db.session.delete(agency)
            db.session.commit()
            flash('Agency {} was deleted successfully.'.format(agency.name))
        return redirect(url_for("admin.list_agencies"))

    return render_template("admin/detail_agency.html", form=form)


@admin.route('/agency/list', methods=['GET'])
@admin.route('/agency/list/<int:page>', methods=['GET', 'POST'])
@login_required
def list_agencies(page=1):
    agencies = Agency.query.paginate(page, 10, False)
    return render_template("admin/list_agencies.html", agencies=agencies)


@admin.route('/agent/list', methods=['GET'])
@admin.route('/agent/list/<int:page>', methods=['GET', 'POST'])
@login_required
def list_agents(page=1):
    agents = User.query.filter_by(role_id=Role.AGENT).paginate(page, 10, False)
    return render_template("admin/list_agents.html", agents=agents)
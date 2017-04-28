from __future__ import (absolute_import, division, print_function)

from odm2api.ODMconnection import dbconnection
from odm2api.ODM2.services.readService import ReadODM2
from odm2api.ODM2 import models as odm2_model

from wof.dao import BaseDao
import wof.examples.flask.odm2.timeseries.sqlalch_odm2_models as model


class Odm2Dao(BaseDao):
    def __init__(self, engine, address, db=None, user=None, password=None):

        self.session_factory = dbconnection.createConnection(engine, address, db, user, password)
        self.read = ReadODM2(self.session_factory)
        self.db_session = self.session_factory.getSession()

    def __del__(self):
        self.db_session.close()

    def get_all_sites(self):
        s_rArr = self.read.getSamplingFeatures(type='Site')
        s_Arr = []
        for s_r in s_rArr:
            s = model.Site(s_r)
            s_Arr.append(s)

        return s_Arr

    def get_site_by_code(self, site_code):
        w_s = None
        try:
            s = self.read.getSamplingFeatures(type='Site', codes=[site_code])
        except:
            s = None
        if s is not None:
            w_s = model.Site(s[0])
        return w_s

    def get_sites_by_codes(self, site_codes_arr):
        s_arr = []
        s_rArr = self.read.getSamplingFeatures(type='Site', codes=site_codes_arr)
        for s in s_rArr:
            w_s = model.Site(s)
            s_arr.append(w_s)
        return s_arr

    def get_sites_by_box(self, west, south, east, north):
        """
        north - ymax - latitude
        south - ymin - latitude
        west - xmin - longitude
        east - xmax - longitude
        """
        s_rArr = []
        s_all = self.read.getSamplingFeatures(type='Site')
        # Perform filtering
        for s in s_all:
            if s.Latitude >= south and s.Latitude <= north and s.Longitude >= west and s.Longitude <= east:
                s_rArr.append(s)

        s_Arr = []
        for s_r in s_rArr:
            s = model.Site(s_r)
            s_Arr.append(s)
        return s_Arr

    def get_variables_from_results(self, var_codes=None):
        v_arr = []
        # first get timeseries results
        tsr = [r for r in self.read.getResults() if r.ResultTypeCV == 'Time series coverage']
        if var_codes is not None:
            tsr = [ts for ts in tsr if ts.VariableObj.VariableCode in var_codes]
        for ts in tsr:
            v = ts.VariableObj
            VarSampleMedium = ts.SampledMediumCV
            v_unit = ts.UnitsObj

            r_vals = self.read.getResultValues(ts.ResultID)
            uid = r_vals['TimeAggregationIntervalUnitsID'].unique()[0]

            v_tunit = self.read.getUnits(ids=[int(uid)])[0]
            v_timeinterval = float(r_vals['TimeAggregationInterval'].unique()[0])

            w_v = model.Variable(v, VarSampleMedium, v_unit, v_tunit, v_timeinterval)
            v_arr.append(w_v)

        return v_arr

    def get_all_variables(self):
        v_arr = self.get_variables_from_results()
        return v_arr

    def get_variable_by_code(self, var_code):
        v_arr = self.get_variables_from_results(var_codes=[var_code])
        return v_arr

    def get_variables_by_codes(self, var_codes):
        v_arr = self.get_variables_from_results(var_codes)
        return v_arr

    def get_series_by_sitecode(self, site_code):
        r_arr = []
        tsr = [r for r in self.read.getResults() if r.ResultTypeCV == 'Time series coverage']
        filt_tsr = [r for r in tsr if
                    r.FeatureActionObj.SamplingFeatureObj.SamplingFeatureCode in [site_code]]
        for r in filt_tsr:
            aff = None
            if r.FeatureActionObj.ActionObj.MethodObj.OrganizationObj is not None:
                aff = self.read.getAffiliations(
                    orgcode=r.FeatureActionObj.ActionObj.MethodObj.OrganizationObj.OrganizationCode)  # noqa
            w_r = model.Series(r, aff)
            r_arr.append(w_r)

        return r_arr

    def get_series_by_sitecode_and_varcode(self, site_code, var_code):
        r_arr = []
        tsr = [r for r in self.read.getResults() if r.ResultTypeCV == 'Time series coverage']
        filt_tsr = [r for r in tsr if r.FeatureActionObj.SamplingFeatureObj.SamplingFeatureCode in [
            site_code] and r.VariableObj.VariableCode in [var_code]]  # noqa
        for r in filt_tsr:
            aff = None
            if r.FeatureActionObj.ActionObj.MethodObj.OrganizationObj is not None:
                aff = self.read.getAffiliations(
                    orgcode=r.FeatureActionObj.ActionObj.MethodObj.OrganizationObj.OrganizationCode)
            w_r = model.Series(r, aff)
            r_arr.append(w_r)

        return r_arr

    def get_datavalues(self, site_code,
                       var_code,
                       begin_date_time=None,
                       end_date_time=None):
        r_arr = []
        tsr = [r for r in self.read.getResults() if r.ResultTypeCV == 'Time series coverage']
        filt_tsr = [r for r in tsr if r.FeatureActionObj.SamplingFeatureObj.SamplingFeatureCode in [
            site_code] and r.VariableObj.VariableCode in [var_code]]
        for r in filt_tsr:
            aff = None
            if r.FeatureActionObj.ActionObj.MethodObj.OrganizationObj is not None:
                aff = self.read.getAffiliations(
                    orgcode=r.FeatureActionObj.ActionObj.MethodObj.OrganizationObj.OrganizationCode)
            rvals = self.read.getResultValues(resultid=r.ResultID, starttime=begin_date_time,
                                              endtime=end_date_time)
            for i, rv in rvals.iterrows():
                trv = self.db_session.query(odm2_model.TimeSeriesResultValues).filter_by(
                    ValueID=rv.ValueID).one()
                w_r = model.DataValue(trv, aff)
                r_arr.append(w_r)

        return r_arr

    def get_method_by_id(self, method_id):
        m = self.read.getMethods(ids=[method_id])
        w_m = model.Method(m[0])
        return w_m

    def get_methods_by_ids(self, method_id_arr):
        m = self.read.getMethods(ids=method_id_arr)
        m_arr = []
        for i in m:
            w_m = model.Method(i)
            m_arr.append(w_m)
        return m_arr

    def get_source_by_id(self, source_id):
        aff = self.read.getAffiliations(ids=[source_id])
        w_aff = model.Source(aff[0])
        return w_aff

    def get_sources_by_ids(self, source_id_arr):
        aff = self.read.getAffiliations(ids=source_id_arr)
        aff_arr = []
        for a in aff:
            w_a = model.Source(a)
            aff_arr.append(w_a)
        return aff_arr

    def get_qualcontrollvl_by_id(self, qual_control_lvl_id):
        pl = self.db_session.query(odm2_model.ProcessingLevels) \
            .filter(odm2_model.ProcessingLevels.ProcessingLevelID == qual_control_lvl_id).first()
        w_pl = model.QualityControlLevel(pl)
        return w_pl

    def get_qualcontrollvls_by_ids(self, qual_control_lvl_id_arr):
        pl = self.db_session.query(odm2_model.ProcessingLevels) \
            .filter(
            odm2_model.ProcessingLevels.ProcessingLevelID.in_(qual_control_lvl_id_arr)).all()
        pl_arr = []
        for i in range(len(pl)):
            w_pl = model.QualityControlLevel(pl[i])
            pl_arr.append(w_pl)
        return pl_arr

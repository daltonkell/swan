#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, timezone
import json
from marshmallow import Schema, fields

#==============================================================================
# class DataSchema(Schema):
#     name = fields.Str()
#     values = fields.List(fields.Number())
# 
#==============================================================================

class LocationSchema(Schema):
    name = fields.Str()
    latitude = fields.Float()
    longitude = fields.Float()

class ForecastSchema(Schema):
    source = fields.Str()
    location = fields.Nested(LocationSchema, many=False)
    initialized = fields.DateTime()
    valid = fields.Dict()

forecast_schema = ForecastSchema()

def main():

    import numpy as np
    import pandas as pd

    # forecasts
    forecasts = []

    # for each location (station or warning area)
    #     if warning area, we don't need coordinates
    for l in [('LocationA', 25.001, 55.001), ('LocationB', 25.25, 55.25 )]:

        # model initialization time
        init = datetime.now(timezone.utc).replace(hour=0,minute=0,second=0,microsecond=0)
# this returns the current local dateime, with tzinfo None 
        
#==============================================================================
#         # forecast
#         valid = pd.date_range(init, init+timedelta(days=5), freq="1H")
#         fields = ['wave_height']
#         forecast = dict(
#             source = 'DMOFS', # this is made up, just so we track what model/suite made this
#             location = dict(
#                 name = l[0],
#                 latitude = l[1],  # we'll need to make sure schema accepts None for warnings and doesn't include in output
#                 longitude = l[2]  # we'll need to make sure schema accepts None for warnings and doesn't include in output
#             ),
#             initialized = init,
#             # this is the hack, valid is a dict
#             valid = {v.isoformat(): {n: np.random.random() for n in fields} for v in valid}
# 
#         )
#         forecasts.append(forecast_schema.dump(forecast).data)
#==============================================================================

        # warning
        valid = pd.date_range(init, init+timedelta(days=5), freq="6H")
        fields = ['wave_warning']
        forecast = dict(
            source = 'DMOFS',
            location = dict(
                name = l[0],
                latitude = l[1],
                longitude = l[2]
            ),
            initialized = init,
            valid = {v.isoformat(): {n: np.random.randint(0, 3) for n in fields} for v in valid}
        )
        forecasts.append(forecast_scframe[l] for n in fieldshema.dump(forecast).data)


    print(json.dumps(forecasts, sort_keys=True))

if __name__ == '__main__':
    main()

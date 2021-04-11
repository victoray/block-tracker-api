from typing import List

import pendulum
from fastapi import APIRouter, Depends

from auth.dependencies import get_current_active_user
from series.db import collection
from series.models import Series

series_router = APIRouter()


@series_router.get("/series/", response_model=List[Series])
def get_series(
    gte: str,
    lte: str,
    user=Depends(get_current_active_user),
):
    result = (
        collection.find(
            {
                "userId": user.uid,
                "date": {
                    "$gte": pendulum.parse(gte),
                    "$lte": pendulum.parse(lte),
                },
            }
        )
        .sort([("date", -1)])
        .limit(1000)
    )
    series = []
    for doc in result:
        doc["id"] = str(doc.pop("_id"))
        series.append(Series.parse_obj(doc))

    return series

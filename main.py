from flask import Flask, request, jsonify, Response
from flask.views import MethodView
from models import Session, Advertisement


app = Flask("app")


class HttpError(Exception):
    def __init__(self, status_code: int, error_message: str | dict):
        self.status_code = status_code
        self.error_message = error_message


@app.errorhandler(HttpError)
def error_handler(err: HttpError):
    json_response = jsonify({"error": err.error_message})
    json_response.status_code = err.status_code
    return json_response



@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response: Response):
    request.session.close()
    return response


def get_ads(ad_id):
    ad = request.session.get(Advertisement, ad_id)
    if ad is None:
        raise HttpError(404, "advertisement not found")
    return ad


class AdsView(MethodView):

    @property
    def session(self) -> Session:
        return request.session

    def get(self, ad_id):
        ad = get_ads(ad_id)
        return jsonify(ad.json)


    def post(self):
        json_data = request.json
        ad = Advertisement(
            title=json_data['title'],
            description=json_data['description'],
            owner=json_data['owner']
        )
        self.session.add(ad)
        self.session.commit()
        return jsonify(ad.json)

    def delete(self, ad_id):
        ad = get_ads(ad_id)
        self.session.delete(ad)
        self.session.commit()
        return jsonify({'status': 'deleted'})


ads_view = AdsView.as_view("ads")

app.add_url_rule("/ads/", view_func=ads_view, methods=["POST"])
app.add_url_rule("/ads/<int:ad_id>/", view_func=ads_view, methods=["GET", "DELETE"])

app.run()

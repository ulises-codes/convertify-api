from flask import Flask, jsonify, request, make_response
from convertify.data.convert import convert, UNIT_MAP, UNIT_TYPES
from flask_cors import CORS
import os

client_endpoint = os.environ['CLIENT_ENDPOINT']

application = Flask(__name__)
CORS(application, origin=client_endpoint, methods=["GET", "POST"])


@application.route("/categories")
def get_all_categories():
    return jsonify({'categories': UNIT_TYPES})


@application.route('/categories/<category>')
def query(category):
    units_for_category = {}

    for unit in UNIT_MAP[category]:
        if unit in units_for_category:
            continue

        for to_unit in UNIT_MAP[category][unit]:
            units_for_category[unit] = UNIT_MAP[category][unit][to_unit]['from']
            break

    result = {}

    if request.args:
        if 'from' in request.args and 'to' in request.args and 'amount' in request.args:
            from_unit = request.args['from']
            to = request.args['to']
            amount = float(request.args['amount'])

            if from_unit in units_for_category and to in units_for_category:
                result['result'] = str(convert(
                    unit_type=category, from_unit=from_unit, to=to,
                    amount=amount))

                return jsonify(result)
            else:
                return make_response(
                    jsonify(
                        {'error': 'Invalid parameters'},
                    ), 400)
        else:
            return make_response(jsonify({'error': 'Incomplete parameters'}))

    return jsonify(units_for_category)


if __name__ == "__main__":
    application.run(port=9999)

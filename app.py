from flask import Flask, jsonify
from flask_restx import Resource, Api
from crawling import data_name, scrape_one, scrape

app = Flask(__name__)
api = Api(app)


@api.route('/air/<string:sido>')
class Air_sido(Resource):
    def get(self, sido):
        response = {}
        row = []
        response['Area'] = sido
        data_lists = scrape(sido)

        for data_list in data_lists:
            semi_result = {}
            for i in range(len(data_list)):
                semi_result[data_name[i]] = data_list[i]
            row.append(semi_result)

        response['row'] = row

        return jsonify(response)


@api.route('/air/<string:sido>/<string:loc>')
class Air_loc(Resource):
    def get(self, sido, loc):
        response = {}
        row = []
        response['Area'] = sido
        response['Location'] = loc

        data_list = scrape(sido, loc)
        for i in range(1, len(data_list)):
            semi_result = {}
            semi_result['time'] = data_name[i]
            semi_result['PM2.5'] = data_list[i]['PM2.5']
            semi_result['PM10'] = data_list[i]['PM10']
            row.append(semi_result)
        response['row'] = row

        return jsonify(response)


@api.route('/air/<string:sido>/<string:loc>/<int:hour>')
class Air_loc_hour(Resource):
    def get(self, sido, loc, hour):
        response = {}
        response['Area'] = sido
        response['Location'] = loc
        response['Hour'] = hour

        data_list = scrape(sido, loc)
        response['PM2.5'] = data_list[hour+3]['PM2.5']
        response['PM10'] = data_list[hour+3]['PM10']

        return jsonify(response)


@api.route('/air/<string:sido>/<string:loc>/latestData')
class Air_loc_now(Resource):
    def get(self, sido, loc):
        response = {}
        response['Area'] = sido
        response['Location'] = loc

        data_list = scrape(sido, loc)

        # find the latest updated index
        i = 4
        while (data_list[i]['PM2.5'] != ''):
            i += 1

        response['Hour'] = i-4
        response['PM2.5'] = data_list[i-1]['PM2.5']
        response['PM10'] = data_list[i-1]['PM10']

        return jsonify(response)


@api.route('/air/<string:sido>/<string:loc>/<string:item>')
class Air_loc_item(Resource):
    def get(self, sido, loc, item):
        response = {}
        response['Area'] = sido
        response['Location'] = loc
        response['Item'] = item

        data_list = scrape_one(sido, loc, item)
        for i in range(len(data_list)):
            response[data_name[i]] = data_list[i]

        return jsonify(response)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

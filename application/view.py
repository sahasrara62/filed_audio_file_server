from flask import Blueprint, request, jsonify
from application.audio import audiofiletype
from application.databases import db

import datetime

blueprint = Blueprint("view", __name__, url_prefix="/")


# @blueprint.route("/create", methods=['POST'])
# def create():
# 	if request.method == 'POST':
# 		# return str(request.json)
# 		data = request.json
# 		type = data.get('audioFileType')
#
# 		print(data, type, "#########"*3)
# 		# return data, type
# 		audio_type = None
# 		if audiofiletype.get(type) is None:
# 			return "bad request", 400
# 		audio_type = audiofiletype.get(type)
# 		metadata = data.get("audioFileMetadata")
#
# 		if metadata.get('duration_time') < 0:
# 			metadata['duration_time'] = 0
# 		upload_time = None
# 		current_time = datetime.datetime.utcnow()
# 		try:
# 			upload_time = datetime.datetime.strptime(metadata['uploaded_time'], "%d/%m/%Y %H:%M:%S")
# 			if (upload_time.year == current_time.year) and (upload_time.month == current_time.month) and (
# 					upload_time.date == current_time.date):
# 				pass
# 			else:
# 				metadata['uploaded_time'] = current_time
# 		except:
# 			upload_time = current_time
# 			metadata['uploaded_time'] = current_time
# 		if type =='podcast':
# 			if len(metadata['participents'])>10 or any(i for i in metadata['participents'] if len(i)>100):
# 				return "Bad request, invalid metadata", 400
#
# 		data_obj = None
# 		try:
# 			data_obj = audio_type(**metadata)
# 			db.session.add(data_obj)
# 			db.session.commit()
# 			db.session.close()
# 			print("added in the database")
# 		except:
# 			print("error occur")
# 			db.session.rollback()
# 			return "Bad request, invalid metadata", 400
# 		return "successfuly inserted", 200
# 	return "invalid request type", 400
#
#
# @blueprint.route("/api/v1/curd/<audioFileType>", methods=['GET'], defaults={"audioFileID": None})
# @blueprint.route("/api/v1/curd/<audioFileType>/<audioFileID>", methods=['PUT', 'DELETE', 'GET'])
# def audio_curd(audioFileType, audioFileID):
# 	if request.method == 'PUT':
# 		data = request.json
# 		print(data)
# 		if audioFileType not in audiofiletype:
# 			return "bad request", 400
# 		audio_file = audiofiletype.get(audioFileType)
# 		metadata = data.get("audioFileMetadata")
# 		metadata['uploaded_time'] = datetime.datetime.utcnow()
# 		try:
# 			audiodata = audio_file.query.filter_by(id=int(audioFileID))
# 			audiodata.update(dict(metadata))
# 			db.session.commit()
# 			db.session.close()
# 			print(audio_file.query.filter_by(id=int(audioFileID)).one().as_dict())
# 			return "ok 200", 200
# 		except:
# 			db.session.rollback()
# 			return "invalid metadata", 400
# 	elif request.method == 'DELETE':
# 		data = request.json
#
# 		if audioFileType not in audiofiletype:
# 			return "bad request", 400
# 		audio_file = audiofiletype.get(audioFileType)
#
# 		try:
# 			id_ = audio_file.query.filter_by(id=int(audioFileID)).one()
# 			db.session.delete(id_)
# 			db.session.commit()
# 			db.session.close()
# 			return "ok", 200
# 		except:
# 			db.session.rollback()
# 			return "invalid id", 400
# 	elif request.method == 'GET':
# 		print(audiofiletype, audioFileID)
# 		data = request.json
# 		if audioFileType not in audiofiletype:
# 			return "bad request", 400
# 		audio_file = audiofiletype.get(audioFileType)
# 		result = None
# 		try:
#
# 			if audioFileID is None:
# 				result = audio_file.query.all()
# 				result = [i.as_dict() for i in result]
# 			else:
# 				result = audio_file.query.filter_by(id=int(audioFileID)).one()
# 				result = [result.as_dict()]
# 			return jsonify({"data":result})
# 		except :
# 			return "invalid metadata", 400
# 	return "error ", 500


@blueprint.route("/")
def home():
    return "server is runnin"


@blueprint.route("/api/v1/create", methods=["POST"])
def create_api():
    if request.method == "POST":

        data = request.json
        type = data.get("audioFileType", None)

        if type is None:
            return "The request is invalid: 400 bad request", 400
        audio_type = audiofiletype.get(type)
        metadata = data.get("audioFileMetadata")

        # check duration time and upload time
        if metadata["duration_time"] <= 0:
            metadata["duration_time"] = 0
        metadata["uploaded_time"] = datetime.datetime.utcnow()
        if type == "podcast":
            participent = metadata.get("participents", None)
            if (
                participent is None
                or len(participent) > 10
                or any(i for i in participent if len(i) > 100)
            ):
                return "The request is invalid: 400 bad request", 400
        try:
            audio_obj = audio_type(**metadata)
            db.session.add(audio_obj)
            db.session.commit()
            db.session.close()
            return "200 ok", 200
        except:
            return "The request is invalid: 400 bad request", 400
    return "The request is invalid: 400 bad request", 400


@blueprint.route("/api/v1/update/<audioFileType>/<audioFileID>", methods=["PUT"])
def update_api(audioFileType, audioFileID):
    if request.method == "PUT":
        request_data = request.json
        if audioFileType not in audiofiletype:
            return "The request is invalid: 400 bad request", 400
        audio_file_obj = audiofiletype.get(audioFileType)
        metadata = request_data.get("audioFileMetadata")
        metadata["uploaded_time"] = datetime.datetime.utcnow()
        try:
            audio_obj = audio_file_obj.query.filter_by(id=int(audioFileID))
            if not metadata:
                return "The request is invalid: 400 bad request", 400

            audio_obj.update(dict(metadata))
            db.session.commit()
            db.session.close()
            return "200 ok", 200
        except:
            return "The request is invalid: 400 bad request", 200
    return "The request is invalid: 400 bad request", 400


@blueprint.route("/api/v1/delete/<audioFileType>/<audioFileID>", methods=["DELETE"])
def delete_api(audioFileType, audioFileID):
    if request.method == "DELETE":

        if audioFileType not in audiofiletype:
            return "The request is invalid: 400 bad request", 400
        audio_file_obj = audiofiletype.get(audioFileType)
        try:
            audio_obj = audio_file_obj.query.filter_by(id=int(audioFileID))
            if not audio_obj.one():
                return "The request is invalid: 400 bad request", 400
            audio_obj.delete()
            db.session.commit()
            db.session.close()
            return "200 ok", 200
        except:
            return "The request is invalid: 400 bad request", 400
    return "The request is invalid: 400 bad request", 400


@blueprint.route(
    "/api/v1/get/<audioFileType>", methods=["GET"], defaults={"audioFileID": None}
)
@blueprint.route("/api/v1/get/<audioFileType>/<audioFileID>", methods=["GET"])
def get_api(audioFileType, audioFileID):
    if request.method == "GET":
        if audioFileType not in audiofiletype:
            return "The request is invalid: 400 bad request", 400
        audio_obj = audiofiletype.get(audioFileType)
        data = None
        try:
            if audioFileID is not None:
                data = audio_obj.query.filter_by(id=int(audioFileID)).one()
                data = [data.as_dict()]
            else:
                data = audio_obj.query.all()
                data = [i.as_dict() for i in data]
            return jsonify({"data": data}), 200
        except:
            return "The request is invalid: 400 bad request", 400
    return "The request is invalid: 400 bad request", 400

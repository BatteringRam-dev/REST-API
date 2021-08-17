from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {likes})"

db.create_all()

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)  #What help value does is what we should display to the sender if they dont send us the name argument
video_put_args.add_argument("views", type=int, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="Views of the video")
video_update_args.add_argument("likes", type=int, help="Likes on the video")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

class Video(Resource):
    @marshal_with(resource_fields)  #What the resource fields does is it serializes the result into json format
    def get(self, video_id):       #We can use many requests when using a resource such as get, post etc.
        result = VideoModel.query.filter_by(id=video_id).first()  #Filter all of the videos we have by ID and return the first response
        if not result:
            abort(404, message="Could not find video with that id")
        return result

    @marshal_with(resource_fields)
    def put(self, video_id):                #Whatever videoid they pass in the put request, we are going to make that the video id
        args = video_put_args.parse_args()  #Args removes errors
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(400, message="Video id taken...")

        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201  #201 means that's created

    @marshal_with(resource_fields)
    def patch(self, video_id):                   #Updating requests
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video doesnt exist, cannot update")

        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']

        db.session.commit()

        return result

    def delete(self, video_id):
        abort_if_video_id_doesnt_exist(video_id)
        del videos[video_id]
        return '', 204                              #204 stands for deleted successfully

api.add_resource(Video, "/video/<int:video_id>")    #Making parameters inside that is passing in parameters

if __name__ == "__main__":
    app.run(debug=True)
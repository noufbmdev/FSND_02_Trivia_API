import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    # This class represents the trivia test case

    def setUp(self):
        # Define test variables and initialize app.
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        categories = Category.query.all()
        num_of_categories = len(categories)

        response = self.client().get("/categories")
        data = json.loads(response.data.decode())

        if num_of_categories > 0:
            formatted_categories = [category.format() for category
                                    in categories]
            same_list = all(data["categories"][i] == formatted_categories[i]
                            for i in range(0, num_of_categories))

            self.assertEqual(response.status_code, 200)
            self.assertTrue(isinstance(data["categories"], list))
            self.assertTrue(same_list)
            self.assertEqual(len(data["categories"]), num_of_categories)
        else:
            self.assertEqual(response.status_code, 404)
            self.assertFalse(data["success"])
            self.assertEqual(data["message"], "Resource not found.")

    def test_update_question_valid_id(self):
        question_id = str(Question.query.with_entities(Question.id).first())[0]

        response = self.client().patch("/questions/" + question_id,
                                       data=json.dumps(dict(category='2')),
                                       content_type='application/json')
        data = json.loads(response.data.decode())

        if question_id > '0':
            questions_category = Question.query.with_entities(
                Question.category).filter_by(
                id=question_id).one_or_none()[0]

            self.assertEqual(response.status_code, 200)
            self.assertTrue(data["success"])
            self.assertEqual("2", questions_category)
        else:
            self.assertEqual(response.status_code, 404)
            self.assertFalse(data["success"])
            self.assertEqual(data["message"], "Resource not found.")

    def test_update_question_invalid_id(self):
        question_id = str(Question.query.count() * 10)
        response = self.client().patch("/questions/" + question_id,
                                       data=json.dumps(dict(category='2')),
                                       content_type='application/json')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Resource not found.")

    def test_get_questions(self):
        response = self.client().get("/questions?page=1")
        data = json.loads(response.data.decode())

        total_num_of_questions = Question.query.count()
        at_most_10_questions = False

        if len(data["questions"]) <= 10:
            at_most_10_questions = True

        num_of_categories = Category.query.count()

        if total_num_of_questions > 0:
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data["success"])
            self.assertTrue(isinstance(data["questions"], list))
            self.assertTrue(at_most_10_questions)
            self.assertEqual(data["total_questions"], total_num_of_questions)
            self.assertTrue(isinstance(data["categories"], list))
            self.assertEqual(len(data["categories"]), num_of_categories)
        else:
            self.assertEqual(response.status_code, 404)
            self.assertFalse(data["success"])
            self.assertEqual(data["message"], "Resource not found.")

    def test_delete_question_valid_id(self):
        question_id = Question.query.with_entities(Question.id).first()[0]
        all_questions_ids = Question.query.with_entities(Question.id).all()

        response = self.client().delete("/questions/" + str(question_id))
        data = json.loads(response.data.decode())

        if question_id > 0:
            if question_id not in all_questions_ids:
                question_deleted = True
            else:
                question_deleted = False

            self.assertEqual(response.status_code, 200)
            self.assertTrue(data["success"])
            self.assertTrue(question_deleted)
            self.assertEqual(data["total_num_of_questions"],
                             (Question.query.count()))
        else:
            self.assertEqual(response.status_code, 422)
            self.assertFalse(data["success"])
            self.assertEqual(data["message"], "Unprocessable entity.")

    def test_delete_question_invalid_id(self):
        total_questions_plus_1 = str(Question.query.count() * 10)
        response = self.client().delete("/questions/" + total_questions_plus_1)
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Unprocessable entity.")

    def test_add_question(self):
        response = self.client().post("/questions",
                                      data=json.dumps(dict(question='test',
                                                      answer='test',
                                                      difficulty=4,
                                                      category='2')),
                                      content_type='application/json')
        data = json.loads(response.data.decode())

        question = Question.query.filter_by(
                          id=data["created_question"]["id"]).one_or_none()

        # Test the json data is correct.
        if (data["created_question"]["question"] == 'test'
           and data["created_question"]["answer"] == 'test'
           and data["created_question"]["difficulty"] == 4
           and data["created_question"]["category"] == '2'):
            same_question = True
        else:
            same_question = False

        # Test the data have been inserted into the database.
        if (question.question == 'test'
           and question.answer == 'test'
           and question.difficulty == 4
           and question.category == '2'):
            same_question = True
        else:
            same_question = False

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(same_question)
        self.assertEqual(data["total_num_of_questions"],
                         len(Question.query.all()))

    def test_search(self):
        search_term = "test"
        response = self.client().post("/questions",
                                      data=json.dumps(dict(
                                        search_term=search_term)),
                                      content_type='application/json')
        data = json.loads(response.data.decode())

        questions = Question.query.filter(
            Question.question.ilike('%' + search_term + '%')).all()

        search_term_in_questions = all([search_term in
                                        data["questions"][question]["question"]
                                        for question
                                        in range(0, len(data["questions"]))])

        if len(questions) > 0:
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data["success"])
            self.assertTrue(search_term_in_questions)
        else:
            self.assertEqual(response.status_code, 404)
            self.assertFalse(data["success"])
            self.assertEqual(data["message"], "Resource not found.")

    def test_get_category_questions_valid_id(self):
        total_categories = str(Category.query.count())

        response = self.client().get("/categories/" +
                                     total_categories + "/questions")
        data = json.loads(response.data.decode())

        category = Category.query.get(total_categories)

        all_questions_categories = all([data["questions"][question]["category"]
                                        == str(category.id) for question in
                                        data["questions"]])

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(all_questions_categories)
        self.assertEqual(data["total_questions"], Question.query.count())
        self.assertEqual(data["current_category"], category.type)

    def test_get_category_questions_invalid_id(self):
        total_categories_plus_1 = str(Category.query.count() + 1)

        response = self.client().get(
            "/categories/"+total_categories_plus_1+"/questions")
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Resource not found.")

    def test_play_trivia(self):
        response = self.client().post("/trivia",
                                      data=json.dumps(dict(
                                                      previous_questions=[2],
                                                      category=2)),
                                      content_type='application/json')
        data = json.loads(response.data.decode())

        self.assertTrue(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["question"]["category"], "2")
        self.assertEqual(len(data["question"]), 5)

    def test_400_error(self):
        response = self.client().post("/questions")
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Bad Request.")

    def test_404_error(self):
        response = self.client().get("/questions?page=1000")
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Resource not found.")

    def test_422_error(self):
        response = self.client().delete("/questions/1000")
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Unprocessable entity.")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

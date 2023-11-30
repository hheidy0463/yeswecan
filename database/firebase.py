import firebase_admin
from firebase_admin import credentials, firestore

class Firebase:
    def __init__(self):
        cred = credentials.Certificate("firebase_key.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def read_from_document(self, collection_name, document_name):
        doc_ref = self.db.collection(collection_name).document(document_name)
        doc_snapshot = doc_ref.get()

        if doc_snapshot.exists:
            document_data = doc_snapshot.to_dict()
            return document_data
        else:
            raise NameError("The document doesn't exist.")

    def create_lecture(self, class_name, lecture_title, data):
        """Creates a lecture document in Firestore with transcript data."""
        lec_ref = self.db.collection(class_name).document(lecture_title)
        lec_ref.set(dict(data), merge=True)
        

if __name__ == "__main__":
    firestore_client = Firebase()
    # data = {"professor": "DeNero", "transcript": ""}
    # firestore_client.create_lecture("CS 61A", "Databases", data)
    
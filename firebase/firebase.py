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
        
    def write_data_to_collection(self, collection_name, document_name, data):
        doc_ref = self.db.collection(collection_name).document(document_name)
        doc_ref.set(dict(data), merge=True)

if __name__ == "__main__":
    firestore_client= Firebase()
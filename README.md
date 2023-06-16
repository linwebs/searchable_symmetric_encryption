# Searchable Symmetric Encryption

### About
Please refer to the complete project <https://github.com/linwebs/searchable_encryption.git>.

### Solution
Solution of the problem is based on this [article](https://hcis-journal.springeropen.com/articles/10.1186/s13673-015-0039-9).  

Search steps over encrypted data:
1. Create three example json data files. You can create examples if you execute python file _create\_patient\_json.py_. One of examples is shown in the picture.  
![alt json_file](images/json_file.png "JSON file")

2. Create 32B index and document key and save them: _SSE_ class method _generate\_and\_save\_keys_.

3. Generate 16B IVs and update document index - _SSE_ class method _update\_IVs\_and\_doc\_index_.

4. Create switched document index for server - _SSE_ class method _create\_switched\_document\_index_.

5. Create inverted document index - _OPE_ class method _create\_inverted\_keyword\_index_.

6. Create index for all distinct values for every field - _OPE_ class method _create\_index\_of\_values_.

7. Encrypt inverted document index with index key and save it on server - _OPE_ class method _encrypt\_index_.

8. Encrypt all example documents with document key and save it on server - _OPE_ class method _encrypt\_documents_.

9. Search over encrypted data - _OPE_ class methods _generate\_search\_token_ and _search_.

10. Copy encrypted files that fit the query to user - _OPE_ class method _copy\_encrypted\_files\_to\_user_.

11. Decrypt files at user with document key - _OPE_ class method _decrypt\_documents_.


### _Instructions for establishing working directory_

1. Create empty folder and name it for example _TestSSE_.

2. Inside this directory create five more folders and name them _Data_, _Private_, _Server_, _SSE_, _User_.

3. Inside _Private_ directory create empty folders named _keys_ and _IVs_.

4. Inside _Private_ directory create json file _document\_index.json_ with empty brackets {}.

5. Inside _Private/IVs_ directory create json file _ivs.json_ with empty brackets {}.

6. Inside _SSE_ directory copy all files downloaded from github link <https://github.com/linwebs/searchable_symmetric_encryption/tree/web>.

Your directory structure should look something like this:  
![alt folder_structure](images/folder_structure_1.png "directory structure")

7. Inside _SSE/src_ directory execute _create\_patient\_json.py_ file.

8. In terminal move to _SSE/src_ directory, start _ipython_ and execute this commands:
```python
from SSE import SSE
sse = SSE()

sse.generate_and_save_keys()
sse.update_IVs_and_doc_index()
```

After that your directory structure should look something like this:  
![alt folder_structure_2](images/folder_structure_2.png "directory structure")

9. In terminal move to _SSE/src_ directory, start _ipython_ and execute this commands:
```python
from SSE import SSE
from OPE import OPE
sse = SSE()
ope = OPE()

sse.create_switched_document_index()
ope.create_inverted_keyword_index()
```

After that your directory structure should look something like this:  
![alt folder_structure_3](images/folder_structure_3.png "directory structure")

Inverted index should look like this:  
![alt inverted_index](images/inverted_index.png "inverted index")

10. In terminal move to _SSE/src_ directory, start _ipython_ and execute this commands:
```python
from OPE import OPE
ope = OPE()

ope.create_index_of_values()
ope.encrypt_index()
ope.encrypt_documents()
```

11. Inside _User_ directory make two empty directories named _encrypted_ and _decrypted_.

After that your directory structure should look something like this:    
![alt folder_structure_4](images/folder_structure_4.png "directory structure")

Encrypted file of Leach Mcdaniel should look like this:  
![alt encrypted_file](images/encrypted_file.png "Leach Mcdaniel data encrypted")

12. Now we have everything prepared to use website to search over data.


### Website example
![website](images/website.png)

---

In my solution we used Python 3.6.13 and Anaconda 3.

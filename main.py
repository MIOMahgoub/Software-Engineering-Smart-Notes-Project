from fastapi import FastAPI, UploadFile, File
import aiofiles
import os
from pathlib import Path
Smart_Notes_Analyzer_app = FastAPI(title="Welcome to Smart Notes Analyzer")
Download_Dir = Path("Downloads")
Download_Dir.mkdir(exist_ok= True)
@Smart_Notes_Analyzer_app.post("/downloads/")
async def upload_file(file: UploadFile):
    SNA_file_path = Download_Dir / file.filename
    async with aiofiles.open(SNA_file_path, "wb") as new_file:
        document_content = await file.read()
        await new_file.write(document_content)
        print("Results: File Uploaded Successfully!")
    return {"file name": file.filename}


#Ulili, Stanley. “Uploading Files Using FastAPI: A Complete Guide to Secure File Handling | Better Stack Community.” Betterstackhq, 2016, betterstack.com/community/guides/scaling-python/uploading-files-using-fastapi/.
#“Request Files - FastAPI.” Tiangolo.com, 2025, fastapi.tiangolo.com/tutorial/request-files/#uploadfile. Accessed 1 Dec. 2025. 
#GeeksForGeeks. “Save UploadFile in FastAPI.” GeeksForGeeks, 23 July 2025, www.geeksforgeeks.org/python/save-uploadfile-in-fastapi/.
#Agnew, Sam. “Working with Files Asynchronously in Python Using Aiofiles and Asyncio.” DEV Community, 14 Jan. 2025, dev.to/sagnew/working-with-files-asynchronously-in-python-using-aiofiles-and-asyncio-1a4k. Accessed 1 Dec. 2025.
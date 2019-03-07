import os

from aeneas.executetask import ExecuteTask
from aeneas.task import Task

def getAlignmentBatch(mp3sDir, transcriptsDir, outDir):

    for mp3FileName in os.listdir(mp3sDir):
        mp3Path = os.path.join(mp3sDir, mp3FileName)
        base, _ = os.path.splitext(mp3FileName)
        transcriptPath = os.path.join(transcriptsDir, base + '.txt')
        outFilePath = os.path.join(outDir, base + '.csv')

        getAlignment(mp3Path, transcriptPath, outFilePath)

def getAlignment(audioFile, textFile, outFile):
    print('Processing ' + audioFile)
    # create Task object
    config_string = u"task_language=eng|is_text_type=plain|os_task_file_format=csv"
    task = Task(config_string=config_string)
    task.audio_file_path_absolute = audioFile
    task.text_file_path_absolute = textFile
    task.sync_map_file_path_absolute = outFile

    # process Task
    ExecuteTask(task).execute()

    # output sync map to file
    task.output_sync_map_file()

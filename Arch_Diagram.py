## Architecture Diagram
# From diagrams 
from cProfile import label
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.storage import S3
from diagrams.azure.identity import Users
from diagrams.onprem.container import Docker
from diagrams.onprem.workflow import Airflow
from diagrams.custom import Custom
from diagrams.onprem.workflow import Airflow
from diagrams.gcp.compute import Functions as GCF
from diagrams.gcp.devtools import SDK

# Creating the cloud cluster 
with Diagram("Workflow", show=False, direction = "LR"):
    with Cluster("Cloud"):

        # Airflow Process 
        with Cluster("Airflow"):
               adhoc_dag = Airflow("Adhoc Dag Process")
               batch_dag = Airflow("Batch Dag Process")

               with Cluster("Google CLoud Platform"):
                airflow_gcp = GCF("Airflow")
        # Streamlit Appliation 
        with Cluster("Streamlit"):
            with Cluster("Streamlit CLoud"):
                 streamlit_cloud = SDK("Streamlit Cloud")
            streamlit_app = Custom("Streamlit", "./data/streamlit-logo.png")

        with Cluster("API"):
            whisper_api = Custom("Whisper API", r"./data/Rev-AudioTipsandTechniques-1.png")
            chat_api = Custom("Chat API",r"./data/download.png")
        
        # AWS s3 storages
        with Cluster("S3 storages"):
            s3_CGR = S3("ChatGPT Results")
            s3_PT = S3("Processed transcript")
            s3_BAF = S3("Batch Audio Files")
            s3_AF = S3("Raw Audio Files")
            
            
    with Cluster("User"):
        user = Users("User")
    # Flow 1 : User uploads file >> triggering adhoc dag
    user >> Edge(label="Asks question after selecting file",color="blue") >> streamlit_app
    streamlit_app >> Edge(label = "Triggers Adhoc Process",color="blue") >> adhoc_dag
    adhoc_dag >> Edge(label="Stores file in rawmp3 bucket",color="blue") >> s3_AF
    s3_AF >> Edge(label=" Calls Whisper API to generate transcript",color="blue") >> whisper_api
    whisper_api >> Edge(label="Storing processed transcript in s3 bucket",color="blue") >> s3_PT
  
    # Flow 2 : User asks question 
    user >> Edge(label="Uploads File",color="black") >> streamlit_app
    streamlit_app >> Edge(color="black") >> chat_api

    # Flow 3 : Batch Dag
    batch_dag >> Edge(label="Runs every day and stores file in batchmp3 bucket",color="red") >> s3_BAF
    s3_BAF >> Edge(label="Asks Generic questions to Chat API",color="red") >> chat_api
    chat_api >> Edge (label="Stores the chat result in chatgpt_results bucket",color="red") >> s3_CGR
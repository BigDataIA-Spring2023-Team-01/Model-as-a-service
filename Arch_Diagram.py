## Architecture Diagram
# From diagrams 
from cProfile import label
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.storage import S3
from diagrams.onprem.client import User
from diagrams.onprem.container import Docker
from diagrams.onprem.workflow import Airflow
from diagrams.custom import Custom
from diagrams.onprem.workflow import Airflow

# Creating the cloud cluster 
with Diagram("Workflow", show=False, direction = "LR"):
    with Cluster("Cloud"):

        # Airflow Process 
        with Cluster("Airflow"):
               adhoc_dag = Airflow("Adhoc Dag Process")
               batch_dag = Airflow("Batch Dag Process")

            #    with Cluster("Docker"):
            #     airflow_docker = Docker("Airflow")
        # Streamlit Appliation 
        with Cluster("Streamlit"):
            # with Cluster("Docker"):
                # streamlit_docker = Docker("Streamlit")
         streamlit_app = Custom("Streamlit", "./data/streamlit-logo.png")

        with Cluster("API"):
            whisper_api = Custom("Whisper API", r"C:\Users\user\OneDrive\Desktop\DAMG_7245\Model-as-a-service\data\Rev-AudioTipsandTechniques-1.png")
            chat_api = Custom("Chat API",r"C:\Users\user\OneDrive\Desktop\DAMG_7245\Model-as-a-service\data\download.png")
        
        # AWS s3 storages
        with Cluster("Storage"):
            s3_CGR = S3("ChatGPT Results")
            s3_PT = S3("Processed transcript")
            s3_BAF = S3("Batch Audio Files")
            s3_AF = S3("Raw Audio Files")
            
            
    with Cluster("User"):
        user = User("User")
    # Flow 1 : User uploads file >> triggering adhoc dag
    user >> Edge(label="Uploads File") >> streamlit_app
    streamlit_app >> Edge(label = "Triggers Adhoc Process") >> adhoc_dag
    adhoc_dag >> Edge(label="Stores file in rawmp3 bucket") >> s3_AF
    s3_AF >> Edge(label=" Calls Whisper API to generate transcript") >> whisper_api
    whisper_api >> Edge(label="Storing processed transcript in s3 bucket") >> s3_PT
  
    # Flow 2 : User asks question 
    user >> Edge(label="Asks question after selecting file") >> streamlit_app
    streamlit_app >> chat_api

    # Flow 3 : Batch Dag
    batch_dag >> Edge(label="Runs every day and stores file in batchmp3 bucket") >> s3_BAF
    s3_BAF >> Edge(label="Asks Generic questions to Chat API") >> chat_api
    chat_api >> Edge (label="Stores the chat result in chatgpt_results bucket") >> s3_CGR
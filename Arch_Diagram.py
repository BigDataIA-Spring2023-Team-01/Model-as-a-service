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

with Diagram("Whisper and Chat API Architecture", show=False, direction = "LR"):
    with Cluster("Cloud"):
        with Cluster("Airflow"):
               dag_adhoc = Airflow("Adhoc Process")
               dag_batch = Airflow("Batch Process")

               with Cluster("Docker"):
                airflow_docker = Docker("Airflow")

        with Cluster("Streamlit"):
            with Cluster("Docker"):
                streamlit_docker = Docker("Streamlit")
            streamlit_app = Custom("Streamlit", "./streamlit-icon.png")

        with Cluster("API"):
            whisper_api = Custom("Whisper API", "./whisper-icon.png")
            chat_api = Custom("Chat API", "./chatgpt-icon.png")

        with Cluster("Storage"):
            s3 = S3("Audio Files")

    with Cluster("User"):
        user = User("User")

    user >> Edge(label = "Access Echonotes application") >> streamlit_app
    user  >> chat_api 
    s3 >> Edge(label = "Fetches general questionnaire file from S3") >> chat_api
    streamlit_app >> Edge(label = "Triggers Adhoc Process and Uploads audio file") >> dag_adhoc
    dag_adhoc >> Edge(label = "Calls Whisper API to generate transcript") >> whisper_api
    dag_batch >> Edge(label = "Runs every midnight and Stores files in S3") >> s3
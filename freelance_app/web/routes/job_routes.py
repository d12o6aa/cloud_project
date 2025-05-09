from flask import Blueprint, request, render_template
from flask import Blueprint, request, render_template
from app.use_cases.job_use_cases import CreateJob, ListOpenJobs
from infrastructure.repositories.sqlalchemy_repo import SQLAlchemyJobRepo


job_bp = Blueprint("job", __name__)

@job_bp.route("/create_job", methods=["GET", "POST"])
def create_job():
    if request.method == "POST":
        data = request.form
        use_case = CreateJob(SQLAlchemyJobRepo())
        try:
            job = use_case.execute({
                "title": data["title"],
                "description": data["description"],
                "budget": float(data["budget"]),
                "deadline": data["deadline"],
                "client_id": int(data["client_id"])
            })
            return f"Job {job.title} created successfully."
        except Exception as e:
            return f"Error: {str(e)}"
    return render_template("create_job.html")


@job_bp.route("/list_jobs")
def list_jobs():
    use_case = ListOpenJobs(SQLAlchemyJobRepo())
    jobs = use_case.execute()
    return render_template("list_jobs.html", jobs=jobs)
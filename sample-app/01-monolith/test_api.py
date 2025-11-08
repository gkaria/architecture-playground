"""Simple test for the monolith API."""

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["architecture"] == "monolith"
    print("✓ Root endpoint works")


def test_health():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✓ Health check works")


def test_create_task():
    """Test creating a task."""
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "status": "todo",
        "priority": "high",
        "user_id": 1,
        "project_id": 1,
        "tags": ["test", "demo"]
    }
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["status"] == "todo"
    assert "id" in data
    print(f"✓ Task created with ID: {data['id']}")
    return data["id"]


def test_get_tasks():
    """Test getting all tasks."""
    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
    print(f"✓ Retrieved {len(tasks)} tasks")


def test_get_task():
    """Test getting a specific task."""
    # First create a task
    task_id = test_create_task()

    # Then get it
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    print(f"✓ Retrieved task {task_id}")


def test_update_task_status():
    """Test updating task status."""
    # First create a task
    task_id = test_create_task()

    # Update status
    response = client.patch(f"/tasks/{task_id}/status", json={"status": "done"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "done"
    print(f"✓ Updated task {task_id} status to done")


def test_delete_task():
    """Test deleting a task."""
    # First create a task
    task_id = test_create_task()

    # Delete it
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

    # Verify it's gone
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404
    print(f"✓ Deleted task {task_id}")


if __name__ == "__main__":
    print("\n🧪 Running Monolith API Tests\n")
    print("=" * 50)

    test_root()
    test_health()
    test_create_task()
    test_get_tasks()
    test_get_task()
    test_update_task_status()
    test_delete_task()

    print("=" * 50)
    print("\n✅ All tests passed!\n")

# Task Manager UI

**Interactive Task Manager Application** - Experience different architectural patterns through a unified interface.

## What is This?

This is a **common frontend** that connects to different backend implementations of the Task Manager API. It demonstrates that:

- ✅ **Same user experience** across different architectures
- ✅ **Performance differences** between patterns become visible
- ✅ **Architecture is transparent** to the end user
- ✅ **Real-world scenario** - refactor backend without changing UI

## Features

### Core Functionality
- ✅ Create tasks with title, description, priority, and tags
- ✅ View all tasks with real-time status
- ✅ Update task status (To Do → In Progress → Done)
- ✅ Delete tasks
- ✅ Filter tasks by status
- ✅ Live statistics (total, in progress, done)

### Educational Features
- 🎯 **Architecture Selector** - Switch between different backend patterns
- ⚡ **Response Time Tracking** - See performance differences
- 📊 **Real-time Statistics** - Monitor task metrics
- 🎨 **Clean, Modern UI** - Built with Tailwind CSS
- 🔄 **Auto-refresh** - Keep data in sync

## Quick Start

### 1. Start a Backend API

First, start one of the backend implementations:

```bash
# Option 1: Monolithic Architecture (Port 8001)
cd sample-app/01-monolith
python app.py

# Option 2: Other architectures (when implemented)
# cd sample-app/02-modular-monolith && python app.py  # Port 8002
# cd sample-app/03-microservices && python app.py     # Port 8003
```

### 2. Start the UI Server

In a new terminal:

```bash
cd task-manager-ui
python server.py
```

Visit: **http://localhost:9000**

### 3. Use the Application

1. **Select Backend** - Choose architecture from dropdown (currently only Monolith is live)
2. **Create Tasks** - Fill in the form and click "Create Task"
3. **Manage Tasks** - Update status, filter by status, or delete tasks
4. **Watch Metrics** - Observe response times and statistics

## Architecture Selector

The dropdown lets you switch between backend implementations:

| Architecture | Port | Status |
|-------------|------|--------|
| **Monolithic** | 8001 | ✅ Live |
| Modular Monolith | 8002 | 🚧 Coming Soon |
| Microservices | 8003 | 🚧 Coming Soon |
| Event-Driven | 8004 | 🚧 Coming Soon |
| Layered | 8005 | 🚧 Coming Soon |
| Service-Based | 8006 | 🚧 Coming Soon |

## How It Works

### API Communication

The UI communicates with the backend via REST API:

```javascript
// Configuration
const ARCHITECTURES = {
    monolith: { port: 8001, color: 'blue', name: 'Monolithic' },
    // ... other architectures
};

// Dynamic API URL based on selected architecture
function getApiUrl() {
    const arch = ARCHITECTURES[currentArchitecture];
    return `http://localhost:${arch.port}`;
}
```

### API Endpoints Used

- `GET /tasks` - Fetch all tasks
- `POST /tasks` - Create new task
- `PATCH /tasks/{id}/status` - Update task status
- `DELETE /tasks/{id}` - Delete task

### Performance Tracking

Every API call is timed:

```javascript
const startTime = performance.now();
const response = await fetch(`${getApiUrl()}/tasks`);
const endTime = performance.now();
const responseTime = Math.round(endTime - startTime);
```

Response time is displayed in the header to compare architecture performance.

## Technical Stack

- **HTML5** - Semantic markup
- **Tailwind CSS** - Utility-first styling (via CDN)
- **Vanilla JavaScript** - No frameworks, pure JS
- **Fetch API** - Modern HTTP requests
- **Python HTTP Server** - Simple static file serving

## File Structure

```
task-manager-ui/
├── index.html       # Main UI structure
├── app.js           # JavaScript application logic
├── server.py        # Simple Python web server
└── README.md        # This file
```

## Features Breakdown

### 1. Task Creation
- Form validation
- Tag support (comma-separated)
- Priority levels (low/medium/high)
- Default user and project IDs

### 2. Task List
- Card-based layout
- Color-coded status badges
- Priority indicators
- Tag display
- Inline status updates
- Delete functionality

### 3. Filtering
- All tasks
- To Do only
- In Progress only
- Done only

### 4. Statistics
- Total tasks count
- In Progress count
- Done count

### 5. Error Handling
- Connection failures
- HTTP errors
- User-friendly messages
- Retry functionality

## Educational Value

### What Students Learn

1. **Architecture Transparency**
   - Same UI works with different backends
   - Architecture is an implementation detail

2. **Performance Comparison**
   - Monolith: Fast, low latency
   - Microservices: Higher latency, better scalability
   - Event-Driven: Async processing differences

3. **API Design**
   - REST principles
   - HTTP methods
   - Status codes
   - Request/Response patterns

4. **Real-World Patterns**
   - How to refactor backends
   - Maintaining backward compatibility
   - Progressive enhancement

## Tips for Testing

### Performance Comparison

1. Start with Monolith (Port 8001)
2. Create 10 tasks and note response times
3. Switch to another architecture (when available)
4. Repeat same operations
5. Compare response times

### Stress Testing

1. Create many tasks quickly
2. Rapidly switch between filters
3. Test concurrent updates
4. Observe how each architecture handles load

### Error Scenarios

1. Stop the backend server
2. See error handling in UI
3. Restart server
4. Click retry - UI recovers gracefully

## Future Enhancements

When more architectures are implemented:

- 📊 **Side-by-side comparison view**
- 📈 **Performance graphs and charts**
- 🔄 **Live sync between architectures**
- 📝 **Educational annotations** (tooltips explaining what happens)
- ⚡ **Latency simulation** (add artificial delay)
- 🎯 **Load testing tools** (bulk operations)

## Troubleshooting

### Issue: "Failed to connect to API"

**Solution:**
- Make sure backend is running (check terminal)
- Verify port number matches architecture (8001 for monolith)
- Check `http://localhost:8001/docs` - should show API docs

### Issue: Tasks not appearing

**Solution:**
- Click refresh button
- Check browser console for errors
- Verify API is returning data: `curl http://localhost:8001/tasks`

### Issue: CORS errors

**Solution:**
- Not an issue with current setup (same-origin)
- If deploying separately, backend needs CORS headers

## Development

### Local Development

The UI uses vanilla JavaScript - just edit and refresh:

1. Edit `index.html` or `app.js`
2. Refresh browser (no build step needed)
3. Changes are immediately visible

### Adding New Architecture

When you implement a new backend pattern:

1. Update dropdown in `index.html`:
   ```html
   <option value="new-arch" data-port="8007" data-color="teal">New Architecture</option>
   ```

2. Update configuration in `app.js`:
   ```javascript
   const ARCHITECTURES = {
       // ... existing
       'new-arch': { port: 8007, color: 'teal', name: 'New Architecture' }
   };
   ```

3. Remove `disabled` attribute from option
4. Start your new backend on the specified port

## License

Part of the Architecture Patterns Playground project - MIT License

## Questions?

- Check the main project README
- Review the backend API documentation at `/docs`
- Explore the code - it's well-commented!

---

**Learn by building. Understand by comparing.**

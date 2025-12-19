import React, { useState, useEffect } from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '../contexts/AuthContext';
import { useHistory } from '@docusaurus/router';
import { authClient } from '../lib/auth-client';
import TaskList from '../components/tasks/TaskList';
import TaskCreator from '../components/tasks/TaskCreator';
import { Task } from '../components/tasks/TaskCard';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export default function TasksPage() {
  const { user, isLoading: authLoading } = useAuth();
  const history = useHistory();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string>('all');
  const [stats, setStats] = useState({ total: 0, completed: 0, pending: 0, in_progress: 0 });
  const [aiGenerating, setAiGenerating] = useState(false);

  // Redirect if not logged in
  useEffect(() => {
    if (!authLoading && !user) {
      history.push('/login');
    }
  }, [user, authLoading, history]);

  // Fetch tasks
  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await authClient.fetchWithAuth(`${API_URL}/tasks`);

      if (!response.ok) {
        throw new Error('Failed to fetch tasks');
      }

      const data = await response.json();
      setTasks(data.tasks || []);
      setStats({
        total: data.total || 0,
        completed: data.completed || 0,
        pending: data.pending || 0,
        in_progress: data.in_progress || 0
      });
    } catch (error) {
      console.error('Error fetching tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (user) {
      fetchTasks();
    }
  }, [user]);

  // Create task
  const handleCreateTask = async (taskData: any) => {
    try {
      const response = await authClient.fetchWithAuth(`${API_URL}/tasks`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskData),
      });

      if (!response.ok) {
        throw new Error('Failed to create task');
      }

      await fetchTasks();
    } catch (error) {
      console.error('Error creating task:', error);
      throw error;
    }
  };

  // Update task status
  const handleStatusChange = async (taskId: number, newStatus: string) => {
    try {
      const response = await authClient.fetchWithAuth(`${API_URL}/tasks/${taskId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: newStatus }),
      });

      if (!response.ok) {
        throw new Error('Failed to update task');
      }

      await fetchTasks();
    } catch (error) {
      console.error('Error updating task:', error);
    }
  };

  // Delete task
  const handleDeleteTask = async (taskId: number) => {
    try {
      const response = await authClient.fetchWithAuth(`${API_URL}/tasks/${taskId}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error('Failed to delete task');
      }

      await fetchTasks();
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  // Generate AI tasks
  const handleGenerateAITasks = async () => {
    const topic = prompt('Enter a topic for AI task generation (e.g., "ROS2 Basics"):');

    if (!topic) return;

    try {
      setAiGenerating(true);
      const response = await authClient.fetchWithAuth(`${API_URL}/tasks/ai-generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          topic,
          count: 3,
          difficulty: 'medium'
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate AI tasks');
      }

      const data = await response.json();
      alert(`Successfully generated ${data.count} AI tasks!`);
      await fetchTasks();
    } catch (error) {
      console.error('Error generating AI tasks:', error);
      alert('Failed to generate AI tasks. Please try again.');
    } finally {
      setAiGenerating(false);
    }
  };

  if (authLoading || !user) {
    return (
      <Layout title="My Tasks">
        <div className="container margin-vert--xl">
          <div className="text--center">
            <p>Loading...</p>
          </div>
        </div>
      </Layout>
    );
  }

  // Filter tasks
  const filteredTasks = tasks.filter(task => {
    if (filter === 'all') return true;
    return task.status === filter;
  });

  const completionPercentage = stats.total > 0
    ? Math.round((stats.completed / stats.total) * 100)
    : 0;

  return (
    <Layout title="My Tasks" description="Manage your learning tasks">
      <div className="container margin-vert--xl">
        <div className="row">
          <div className="col col--12">
            <h1>My Learning Tasks</h1>
            <p className="hero__subtitle">
              Organize and track your study progress
            </p>
          </div>
        </div>

        {/* Stats */}
        <div className="row margin-top--lg margin-bottom--lg">
          <div className="col col--3">
            <div className="card text--center">
              <div className="card__body">
                <h2>{stats.total}</h2>
                <p>Total Tasks</p>
              </div>
            </div>
          </div>
          <div className="col col--3">
            <div className="card text--center">
              <div className="card__body">
                <h2>{stats.pending}</h2>
                <p>Pending</p>
              </div>
            </div>
          </div>
          <div className="col col--3">
            <div className="card text--center">
              <div className="card__body">
                <h2>{stats.in_progress}</h2>
                <p>In Progress</p>
              </div>
            </div>
          </div>
          <div className="col col--3">
            <div className="card text--center">
              <div className="card__body">
                <h2>{completionPercentage}%</h2>
                <p>Completed</p>
              </div>
            </div>
          </div>
        </div>

        <div className="row">
          <div className="col col--12">
            {/* AI Generate Button */}
            <button
              className="button button--success margin-bottom--md margin-right--sm"
              onClick={handleGenerateAITasks}
              disabled={aiGenerating}
            >
              {aiGenerating ? 'Generating...' : 'Generate AI Tasks ✨'}
            </button>

            {/* Filter Buttons */}
            <div className="margin-bottom--md" style={{ display: 'inline-block' }}>
              <div className="button-group">
                <button
                  className={`button ${filter === 'all' ? 'button--primary' : 'button--outline button--primary'}`}
                  onClick={() => setFilter('all')}
                >
                  All
                </button>
                <button
                  className={`button ${filter === 'pending' ? 'button--warning' : 'button--outline button--warning'}`}
                  onClick={() => setFilter('pending')}
                >
                  Pending
                </button>
                <button
                  className={`button ${filter === 'in_progress' ? 'button--info' : 'button--outline button--info'}`}
                  onClick={() => setFilter('in_progress')}
                >
                  In Progress
                </button>
                <button
                  className={`button ${filter === 'completed' ? 'button--success' : 'button--outline button--success'}`}
                  onClick={() => setFilter('completed')}
                >
                  Completed
                </button>
              </div>
            </div>

            {/* Task Creator */}
            <TaskCreator onCreateTask={handleCreateTask} />

            {/* Task List */}
            {loading ? (
              <div className="text--center">
                <p>Loading tasks...</p>
              </div>
            ) : (
              <TaskList
                tasks={filteredTasks}
                onStatusChange={handleStatusChange}
                onDelete={handleDeleteTask}
                emptyMessage={
                  filter === 'all'
                    ? 'No tasks yet. Create your first task or generate AI tasks!'
                    : `No ${filter.replace('_', ' ')} tasks`
                }
              />
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
}

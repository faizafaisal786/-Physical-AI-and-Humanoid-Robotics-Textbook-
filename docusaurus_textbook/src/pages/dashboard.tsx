import React from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '../contexts/AuthContext';
import { useHistory } from '@docusaurus/router';
import Link from '@docusaurus/Link';
import UserProfile from '../components/UserProfile';

export default function Dashboard() {
  const { user, isLoading } = useAuth();
  const history = useHistory();

  React.useEffect(() => {
    if (!isLoading && !user) {
      history.push('/login');
    }
  }, [user, isLoading, history]);

  if (isLoading) {
    return (
      <Layout title="Dashboard" description="Your personal dashboard">
        <div className="container margin-vert--xl">
          <div className="text--center">
            <p>Loading...</p>
          </div>
        </div>
      </Layout>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <Layout title="Dashboard" description="Your personal dashboard">
      <div className="container margin-vert--xl">
        <div className="row">
          <div className="col col--12">
            <h1>Welcome back, {user.full_name || user.username || 'User'}!</h1>
            <p className="hero__subtitle">
              Track your learning progress and manage your study tasks
            </p>
          </div>
        </div>

        <div className="row margin-top--lg">
          <div className="col col--4">
            <UserProfile />
          </div>

          <div className="col col--8">
            <div className="card margin-bottom--lg">
              <div className="card__header">
                <h3>Quick Actions</h3>
              </div>
              <div className="card__body">
                <div className="row">
                  <div className="col col--6 margin-bottom--md">
                    <Link to="/docs/introduction/intro" className="card card--interactive">
                      <div className="card__body">
                        <h4>Continue Learning</h4>
                        <p>Pick up where you left off</p>
                      </div>
                    </Link>
                  </div>
                  <div className="col col--6 margin-bottom--md">
                    <Link to="/tasks" className="card card--interactive">
                      <div className="card__body">
                        <h4>My Tasks</h4>
                        <p>View and manage your study tasks</p>
                      </div>
                    </Link>
                  </div>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="card__header">
                <h3>Learning Progress</h3>
              </div>
              <div className="card__body">
                <div className="alert alert--info">
                  <strong>Coming Soon!</strong> Track your chapter completion and quiz scores here.
                </div>

                <div className="margin-top--md">
                  <h4>Recent Activity</h4>
                  <p className="text--secondary">
                    Your learning activity will appear here
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}

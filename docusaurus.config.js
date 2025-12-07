/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI Textbook',
  tagline: 'Learn Robotics with ROS2, Gazebo, Unity, and NVIDIA Isaac Sim',
  favicon: 'img/favicon.ico',

  url: 'http://localhost:3000',
  baseUrl: '/',

  organizationName: 'yourusername',
  projectName: 'physical-ai-textbook',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.js',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      },
    ],
  ],
};

export default config;
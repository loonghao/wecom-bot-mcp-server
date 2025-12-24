import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'WeCom Bot MCP Server',
  description: 'A Model Context Protocol (MCP) compliant server for WeCom Bot',
  base: '/wecom-bot-mcp-server/',

  head: [
    ['link', { rel: 'icon', href: '/wecom-bot-mcp-server/favicon.ico' }]
  ],

  locales: {
    root: {
      label: 'English',
      lang: 'en',
      themeConfig: {
        nav: [
          { text: 'Guide', link: '/guide/getting-started' },
          { text: 'Configuration', link: '/config/' },
          { text: 'API', link: '/api/' },
          {
            text: 'Links',
            items: [
              { text: 'PyPI', link: 'https://pypi.org/project/wecom-bot-mcp-server/' },
              { text: 'GitHub', link: 'https://github.com/loonghao/wecom-bot-mcp-server' },
              { text: 'Smithery', link: 'https://smithery.ai/server/wecom-bot-mcp-server' }
            ]
          }
        ],
        sidebar: {
          '/guide/': [
            {
              text: 'Introduction',
              items: [
                { text: 'Getting Started', link: '/guide/getting-started' },
                { text: 'Installation', link: '/guide/installation' },
                { text: 'Quick Start', link: '/guide/quick-start' }
              ]
            },
            {
              text: 'Features',
              items: [
                { text: 'Message Types', link: '/guide/message-types' },
                { text: 'Multi-Bot Support', link: '/guide/multi-bot' }
              ]
            }
          ],
          '/config/': [
            {
              text: 'Configuration',
              items: [
                { text: 'Overview', link: '/config/' },
                { text: 'Environment Variables', link: '/config/environment' },
                { text: 'MCP Clients', link: '/config/mcp-clients' },
                { text: 'Multi-Bot Setup', link: '/config/multi-bot' }
              ]
            }
          ],
          '/api/': [
            {
              text: 'API Reference',
              items: [
                { text: 'Overview', link: '/api/' },
                { text: 'MCP Tools', link: '/api/mcp-tools' },
                { text: 'Python API', link: '/api/python' }
              ]
            }
          ]
        }
      }
    },
    zh: {
      label: '中文',
      lang: 'zh-CN',
      link: '/zh/',
      themeConfig: {
        nav: [
          { text: '指南', link: '/zh/guide/getting-started' },
          { text: '配置', link: '/zh/config/' },
          { text: 'API', link: '/zh/api/' },
          {
            text: '链接',
            items: [
              { text: 'PyPI', link: 'https://pypi.org/project/wecom-bot-mcp-server/' },
              { text: 'GitHub', link: 'https://github.com/loonghao/wecom-bot-mcp-server' },
              { text: 'Smithery', link: 'https://smithery.ai/server/wecom-bot-mcp-server' }
            ]
          }
        ],
        sidebar: {
          '/zh/guide/': [
            {
              text: '介绍',
              items: [
                { text: '快速开始', link: '/zh/guide/getting-started' },
                { text: '安装', link: '/zh/guide/installation' },
                { text: '快速上手', link: '/zh/guide/quick-start' }
              ]
            },
            {
              text: '功能',
              items: [
                { text: '消息类型', link: '/zh/guide/message-types' },
                { text: '多机器人支持', link: '/zh/guide/multi-bot' }
              ]
            }
          ],
          '/zh/config/': [
            {
              text: '配置',
              items: [
                { text: '概述', link: '/zh/config/' },
                { text: '环境变量', link: '/zh/config/environment' },
                { text: 'MCP 客户端', link: '/zh/config/mcp-clients' },
                { text: '多机器人配置', link: '/zh/config/multi-bot' }
              ]
            }
          ],
          '/zh/api/': [
            {
              text: 'API 参考',
              items: [
                { text: '概述', link: '/zh/api/' },
                { text: 'MCP 工具', link: '/zh/api/mcp-tools' },
                { text: 'Python API', link: '/zh/api/python' }
              ]
            }
          ]
        }
      }
    }
  },

  themeConfig: {
    logo: '/logo.png',
    socialLinks: [
      { icon: 'github', link: 'https://github.com/loonghao/wecom-bot-mcp-server' }
    ],
    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2024-present longhao'
    },
    search: {
      provider: 'local'
    }
  }
})

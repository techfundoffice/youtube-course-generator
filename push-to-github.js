import { Octokit } from '@octokit/rest'
import fs from 'fs'
import path from 'path'

let connectionSettings;

async function getAccessToken() {
  if (connectionSettings && connectionSettings.settings.expires_at && new Date(connectionSettings.settings.expires_at).getTime() > Date.now()) {
    return connectionSettings.settings.access_token;
  }
  
  const hostname = process.env.REPLIT_CONNECTORS_HOSTNAME
  const xReplitToken = process.env.REPL_IDENTITY 
    ? 'repl ' + process.env.REPL_IDENTITY 
    : process.env.WEB_REPL_RENEWAL 
    ? 'depl ' + process.env.WEB_REPL_RENEWAL 
    : null;

  if (!xReplitToken) {
    throw new Error('X_REPLIT_TOKEN not found for repl/depl');
  }

  connectionSettings = await fetch(
    'https://' + hostname + '/api/v2/connection?include_secrets=true&connector_names=github',
    {
      headers: {
        'Accept': 'application/json',
        'X_REPLIT_TOKEN': xReplitToken
      }
    }
  ).then(res => res.json()).then(data => data.items?.[0]);

  const accessToken = connectionSettings?.settings?.access_token || connectionSettings.settings?.oauth?.credentials?.access_token;

  if (!connectionSettings || !accessToken) {
    throw new Error('GitHub not connected');
  }
  return accessToken;
}

async function getAllFiles(dir) {
  const files = [];
  const items = fs.readdirSync(dir);
  
  for (const item of items) {
    const fullPath = path.join(dir, item);
    const stat = fs.statSync(fullPath);
    
    // Skip certain directories and files
    if (item.startsWith('.') && item !== '.env.example' && item !== '.gitignore') continue;
    if (['node_modules', '__pycache__', '.git', 'videos', '.upm', '.pythonlibs'].includes(item)) continue;
    if (item.endsWith('.pyc')) continue;
    
    if (stat.isDirectory()) {
      const subFiles = await getAllFiles(fullPath);
      files.push(...subFiles);
    } else {
      const relativePath = path.relative('.', fullPath);
      files.push(relativePath);
    }
  }
  
  return files;
}

async function pushToGitHub() {
  try {
    const octokit = new Octokit({ auth: await getAccessToken() });
    const owner = 'techfundoffice';
    const repo = 'youtube-course-generator';
    
    console.log('📦 Collecting files...');
    const files = await getAllFiles('.');
    console.log(`Found ${files.length} files to push`);
    
    // Get the latest commit SHA for the main branch (or create if doesn't exist)
    let parentSha;
    try {
      const { data: ref } = await octokit.rest.git.getRef({
        owner,
        repo,
        ref: 'heads/main'
      });
      parentSha = ref.object.sha;
    } catch (error) {
      if (error.status === 404) {
        console.log('Main branch does not exist, will create it');
        parentSha = null;
      } else {
        throw error;
      }
    }
    
    console.log('📄 Creating blobs...');
    const blobs = [];
    for (const file of files) {
      try {
        const content = fs.readFileSync(file);
        const { data: blob } = await octokit.rest.git.createBlob({
          owner,
          repo,
          content: content.toString('base64'),
          encoding: 'base64'
        });
        blobs.push({
          path: file,
          mode: '100644',
          type: 'blob',
          sha: blob.sha
        });
        console.log(`✅ ${file}`);
      } catch (error) {
        console.log(`❌ Error with ${file}: ${error.message}`);
      }
    }
    
    console.log('🌳 Creating tree...');
    const { data: tree } = await octokit.rest.git.createTree({
      owner,
      repo,
      tree: blobs,
      base_tree: parentSha
    });
    
    console.log('💾 Creating commit...');
    const { data: commit } = await octokit.rest.git.createCommit({
      owner,
      repo,
      message: `Initial commit - YouTube Course Generator with transcript functionality

Features:
- YouTube video processing with yt-dlp fallback
- AI-powered 7-day course generation  
- Full transcript extraction and display
- Interactive transcript search and download
- Course progress tracking
- Real-time processing logs
- PostgreSQL database with transcript storage`,
      tree: tree.sha,
      parents: parentSha ? [parentSha] : []
    });
    
    console.log('🔄 Updating main branch...');
    if (parentSha) {
      await octokit.rest.git.updateRef({
        owner,
        repo,
        ref: 'heads/main',
        sha: commit.sha
      });
    } else {
      await octokit.rest.git.createRef({
        owner,
        repo,
        ref: 'refs/heads/main',
        sha: commit.sha
      });
    }
    
    console.log('🚀 SUCCESS! Code pushed to GitHub!');
    console.log(`📍 Repository: https://github.com/${owner}/${repo}`);
    console.log(`📋 Commit: ${commit.sha}`);
    
  } catch (error) {
    console.error('❌ Error pushing to GitHub:', error.message);
    throw error;
  }
}

pushToGitHub();
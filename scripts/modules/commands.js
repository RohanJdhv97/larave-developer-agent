/**
 * commands.js
 * Task Master CLI command functionality
 * 
 * This module provides the command line interface functionality,
 * implementing the core commands needed for task management.
 */

import fs from 'fs';
import path from 'path';

// Default paths
const DEFAULT_TASKS_FILE = 'tasks/tasks.json';

/**
 * Run the CLI with the provided arguments
 * @param {string[]} args - Process arguments
 */
export function runCLI(args) {
  const command = args[2];
  
  if (!command) {
    showHelp();
    return;
  }

  // Process commands
  switch (command) {
    case 'list':
      listTasks(args.slice(3));
      break;
    case 'next':
      findNextTask(args.slice(3));
      break;
    case 'show':
      showTask(args.slice(3));
      break;
    case 'set-status':
      setTaskStatus(args.slice(3));
      break;
    case 'help':
    case '--help':
      showHelp();
      break;
    default:
      console.log(`Unknown command: ${command}`);
      console.log('Run "node scripts/dev.js help" for usage information');
      break;
  }
}

/**
 * Parse arguments into an options object
 * @param {string[]} args - Command arguments
 * @returns {Object} - Parsed options
 */
function parseArgs(args) {
  const options = {};
  
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    if (arg.startsWith('--')) {
      const [key, value] = arg.substring(2).split('=');
      options[key] = value || true;
    } else if (arg.startsWith('-')) {
      const key = arg.substring(1);
      options[key] = args[i + 1] || true;
      if (options[key] !== true) {
        i++; // Skip the next argument as it's the value
      }
    } else {
      // Positional argument
      if (!options.positional) {
        options.positional = [];
      }
      options.positional.push(arg);
    }
  }
  
  return options;
}

/**
 * Load tasks from the tasks.json file
 * @param {string} filePath - Path to the tasks file
 * @returns {Object} - Tasks object
 */
function loadTasks(filePath = DEFAULT_TASKS_FILE) {
  try {
    const data = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    console.error(`Error loading tasks file: ${error.message}`);
    process.exit(1);
  }
}

/**
 * List all tasks and their status
 * @param {string[]} args - Command arguments
 */
function listTasks(args) {
  const options = parseArgs(args);
  const tasksFile = options.file || DEFAULT_TASKS_FILE;
  const statusFilter = options.status;
  const withSubtasks = options['with-subtasks'] === true;
  
  const tasksObj = loadTasks(tasksFile);
  const tasks = tasksObj.tasks || [];
  
  console.log('\nTASK LIST\n=========');
  
  const filteredTasks = statusFilter 
    ? tasks.filter(task => task.status === statusFilter)
    : tasks;
  
  if (filteredTasks.length === 0) {
    console.log(`No tasks${statusFilter ? ` with status "${statusFilter}"` : ''} found.`);
    return;
  }
  
  filteredTasks.forEach(task => {
    const dependencies = task.dependencies && task.dependencies.length > 0
      ? ` (depends on: ${task.dependencies.join(', ')})`
      : '';
    
    console.log(`[${task.id}] ${task.title} - ${task.status}${dependencies}`);
    
    if (withSubtasks && task.subtasks && task.subtasks.length > 0) {
      task.subtasks.forEach(subtask => {
        console.log(`  └─ [${task.id}.${subtask.id}] ${subtask.title} - ${subtask.status || 'pending'}`);
      });
    }
  });
  
  console.log(`\nTotal: ${filteredTasks.length} task(s)${statusFilter ? ` with status "${statusFilter}"` : ''}`);
}

/**
 * Find the next task to work on based on dependencies
 * @param {string[]} args - Command arguments
 */
function findNextTask(args) {
  const options = parseArgs(args);
  const tasksFile = options.file || DEFAULT_TASKS_FILE;
  
  const tasksObj = loadTasks(tasksFile);
  const tasks = tasksObj.tasks || [];
  
  // Find all tasks that are pending and have all dependencies completed
  const eligibleTasks = tasks.filter(task => {
    if (task.status !== 'pending') {
      return false;
    }
    
    // Check if all dependencies are marked as done
    if (task.dependencies && task.dependencies.length > 0) {
      const allDependenciesDone = task.dependencies.every(depId => {
        const depTask = tasks.find(t => t.id === depId);
        return depTask && depTask.status === 'done';
      });
      
      return allDependenciesDone;
    }
    
    return true; // No dependencies
  });
  
  if (eligibleTasks.length === 0) {
    console.log('\nNo eligible tasks found. All tasks are either completed or have pending dependencies.');
    return;
  }
  
  // Sort by priority (high > medium > low)
  const priorityOrder = { high: 1, medium: 2, low: 3 };
  eligibleTasks.sort((a, b) => {
    // First by priority
    const priorityA = priorityOrder[a.priority] || 99;
    const priorityB = priorityOrder[b.priority] || 99;
    if (priorityA !== priorityB) {
      return priorityA - priorityB;
    }
    
    // Then by number of dependencies (fewer first)
    const depCountA = (a.dependencies || []).length;
    const depCountB = (b.dependencies || []).length;
    if (depCountA !== depCountB) {
      return depCountA - depCountB;
    }
    
    // Finally by ID (lower first)
    return a.id - b.id;
  });
  
  // Get the top task
  const nextTask = eligibleTasks[0];
  
  console.log('\nNEXT TASK TO IMPLEMENT\n=====================');
  console.log(`[${nextTask.id}] ${nextTask.title} (${nextTask.priority} priority)`);
  console.log(`Status: ${nextTask.status}`);
  
  if (nextTask.dependencies && nextTask.dependencies.length > 0) {
    console.log(`Dependencies: ${nextTask.dependencies.join(', ')} (all satisfied)`);
  } else {
    console.log('Dependencies: none');
  }
  
  console.log('\nDescription:');
  console.log(nextTask.description);
  
  console.log('\nImplementation details:');
  console.log(nextTask.details);
  
  console.log('\nTest strategy:');
  console.log(nextTask.testStrategy || 'No test strategy specified');
  
  if (nextTask.subtasks && nextTask.subtasks.length > 0) {
    console.log('\nSubtasks:');
    nextTask.subtasks.forEach(subtask => {
      console.log(`  [${nextTask.id}.${subtask.id}] ${subtask.title} - ${subtask.status || 'pending'}`);
    });
  }
  
  console.log('\nSuggested actions:');
  console.log(`- Mark as in-progress: node scripts/dev.js set-status --id=${nextTask.id} --status=in-progress`);
  console.log(`- Mark as done when completed: node scripts/dev.js set-status --id=${nextTask.id} --status=done`);
  
  if (!nextTask.subtasks || nextTask.subtasks.length === 0) {
    console.log(`- Expand into subtasks: node scripts/dev.js expand --id=${nextTask.id}`);
  }
}

/**
 * Display detailed information about a specific task
 * @param {string[]} args - Command arguments
 */
function showTask(args) {
  const options = parseArgs(args);
  const tasksFile = options.file || DEFAULT_TASKS_FILE;
  
  // Get task ID from either --id option or first positional argument
  let taskId = options.id;
  if (!taskId && options.positional && options.positional.length > 0) {
    taskId = options.positional[0];
  }
  
  if (!taskId) {
    console.error('Error: Task ID is required. Use --id=<id> or provide it as an argument.');
    return;
  }
  
  const tasksObj = loadTasks(tasksFile);
  const tasks = tasksObj.tasks || [];
  
  // Check if the ID contains a dot, indicating a subtask
  const idParts = taskId.toString().split('.');
  const parentId = parseInt(idParts[0], 10);
  const subtaskId = idParts.length > 1 ? parseInt(idParts[1], 10) : null;
  
  const parentTask = tasks.find(task => task.id === parentId);
  
  if (!parentTask) {
    console.error(`Error: Task with ID ${parentId} not found.`);
    return;
  }
  
  if (subtaskId !== null) {
    // Show subtask
    if (!parentTask.subtasks || parentTask.subtasks.length === 0) {
      console.error(`Error: Task ${parentId} has no subtasks.`);
      return;
    }
    
    const subtask = parentTask.subtasks.find(st => st.id === subtaskId);
    
    if (!subtask) {
      console.error(`Error: Subtask ${parentId}.${subtaskId} not found.`);
      return;
    }
    
    console.log(`\nSUBTASK ${parentId}.${subtaskId}\n=================`);
    console.log(`Title: ${subtask.title}`);
    console.log(`Status: ${subtask.status || 'pending'}`);
    console.log(`Parent task: [${parentTask.id}] ${parentTask.title}`);
    
    if (subtask.dependencies && subtask.dependencies.length > 0) {
      console.log(`Dependencies: ${subtask.dependencies.join(', ')}`);
    }
    
    console.log('\nDescription:');
    console.log(subtask.description);
    
    if (subtask.details) {
      console.log('\nImplementation details:');
      console.log(subtask.details);
    }
    
    console.log('\nSuggested actions:');
    console.log(`- Mark as in-progress: node scripts/dev.js set-status --id=${parentId}.${subtaskId} --status=in-progress`);
    console.log(`- Mark as done when completed: node scripts/dev.js set-status --id=${parentId}.${subtaskId} --status=done`);
    console.log(`- View parent task: node scripts/dev.js show ${parentId}`);
  } else {
    // Show parent task
    console.log(`\nTASK ${parentTask.id}\n========`);
    console.log(`Title: ${parentTask.title}`);
    console.log(`Status: ${parentTask.status}`);
    console.log(`Priority: ${parentTask.priority}`);
    
    if (parentTask.dependencies && parentTask.dependencies.length > 0) {
      console.log(`Dependencies: ${parentTask.dependencies.join(', ')}`);
    } else {
      console.log('Dependencies: none');
    }
    
    console.log('\nDescription:');
    console.log(parentTask.description);
    
    console.log('\nImplementation details:');
    console.log(parentTask.details);
    
    console.log('\nTest strategy:');
    console.log(parentTask.testStrategy || 'No test strategy specified');
    
    if (parentTask.subtasks && parentTask.subtasks.length > 0) {
      console.log('\nSubtasks:');
      parentTask.subtasks.forEach(subtask => {
        console.log(`  [${parentTask.id}.${subtask.id}] ${subtask.title} - ${subtask.status || 'pending'}`);
      });
    } else {
      console.log('\nSubtasks: none');
    }
    
    console.log('\nSuggested actions:');
    console.log(`- Mark as in-progress: node scripts/dev.js set-status --id=${parentTask.id} --status=in-progress`);
    console.log(`- Mark as done when completed: node scripts/dev.js set-status --id=${parentTask.id} --status=done`);
    
    if (!parentTask.subtasks || parentTask.subtasks.length === 0) {
      console.log(`- Expand into subtasks: node scripts/dev.js expand --id=${parentTask.id}`);
    }
  }
}

/**
 * Set the status of a task
 * @param {string[]} args - Command arguments
 */
function setTaskStatus(args) {
  const options = parseArgs(args);
  const tasksFile = options.file || DEFAULT_TASKS_FILE;
  
  if (!options.id) {
    console.error('Error: Task ID is required. Use --id=<id>');
    return;
  }
  
  if (!options.status) {
    console.error('Error: Status is required. Use --status=<status>');
    return;
  }
  
  // Handle multiple IDs separated by commas
  const taskIds = options.id.split(',');
  const status = options.status;
  
  const tasksObj = loadTasks(tasksFile);
  const tasks = tasksObj.tasks || [];
  
  let modified = false;
  
  taskIds.forEach(taskId => {
    // Check if the ID contains a dot, indicating a subtask
    const idParts = taskId.toString().split('.');
    const parentId = parseInt(idParts[0], 10);
    const subtaskId = idParts.length > 1 ? parseInt(idParts[1], 10) : null;
    
    if (subtaskId !== null) {
      // Update subtask status
      const parentTask = tasks.find(task => task.id === parentId);
      
      if (!parentTask) {
        console.error(`Error: Parent task with ID ${parentId} not found.`);
        return;
      }
      
      if (!parentTask.subtasks || parentTask.subtasks.length === 0) {
        console.error(`Error: Task ${parentId} has no subtasks.`);
        return;
      }
      
      const subtask = parentTask.subtasks.find(st => st.id === subtaskId);
      
      if (!subtask) {
        console.error(`Error: Subtask ${parentId}.${subtaskId} not found.`);
        return;
      }
      
      subtask.status = status;
      console.log(`Updated status of subtask ${parentId}.${subtaskId} to "${status}"`);
      modified = true;
    } else {
      // Update parent task status
      const taskIdNum = parseInt(taskId, 10);
      const task = tasks.find(t => t.id === taskIdNum);
      
      if (!task) {
        console.error(`Error: Task with ID ${taskIdNum} not found.`);
        return;
      }
      
      task.status = status;
      console.log(`Updated status of task ${taskIdNum} to "${status}"`);
      
      // If the status is "done", also mark all subtasks as "done"
      if (status === 'done' && task.subtasks && task.subtasks.length > 0) {
        task.subtasks.forEach(subtask => {
          subtask.status = 'done';
        });
        console.log(`Also marked all subtasks of task ${taskIdNum} as "done"`);
      }
      
      modified = true;
    }
  });
  
  if (modified) {
    try {
      fs.writeFileSync(tasksFile, JSON.stringify(tasksObj, null, 2), 'utf8');
      console.log(`Tasks file updated successfully.`);
    } catch (error) {
      console.error(`Error writing tasks file: ${error.message}`);
    }
  }
}

/**
 * Show help message with available commands
 */
function showHelp() {
  console.log(`
Task Master CLI - AI-driven development task management

Usage: node scripts/dev.js [command] [options]

Available commands:
  list                     List all tasks
  next                     Find the next task to work on
  show <id>                Show details of a specific task
  set-status               Change a task's status
  help                     Show this help message

Options for 'list':
  --status=<status>        Filter tasks by status
  --with-subtasks          Include subtasks in the listing
  --file=<path>            Use a different tasks file

Options for 'next':
  --file=<path>            Use a different tasks file

Options for 'show':
  --id=<id>                Task ID to show (can also be provided as positional argument)
  --file=<path>            Use a different tasks file

Options for 'set-status':
  --id=<id>                Task ID or comma-separated IDs to update
  --status=<status>        New status to set
  --file=<path>            Use a different tasks file

Examples:
  node scripts/dev.js list
  node scripts/dev.js list --status=pending
  node scripts/dev.js next
  node scripts/dev.js show 3
  node scripts/dev.js set-status --id=3 --status=done
  `);
} 
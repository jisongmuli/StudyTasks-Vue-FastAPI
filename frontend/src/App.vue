<script setup>
import { computed, onMounted, ref } from 'vue'
import { createTask, deleteTask, getTasks, updateTask } from './api.js'

// ref 保存“页面会变化的数据”；在 JS 里用 .value 读写。
const tasks = ref([])
const newTitle = ref('')
const loading = ref(true)
const saving = ref(false)
const error = ref('')

// computed 根据已有数据计算结果；任务变化时，数量也会自动变化。
const completedCount = computed(() => tasks.value.filter(task => task.completed).length)
const progress = computed(() => tasks.value.length ? completedCount.value / tasks.value.length * 100 : 0)

// 页面刚打开时，先向后端取一次列表。
async function loadTasks() {
  loading.value = true
  error.value = ''
  try {
    tasks.value = await getTasks()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

async function addTask() {
  const title = newTitle.value.trim()
  if (!title || saving.value) return
  saving.value = true
  error.value = ''
  try {
    // 等后端创建成功后，把返回的任务加入页面列表。
    const task = await createTask(title)
    tasks.value.push(task)
    newTitle.value = ''
  } catch (err) {
    error.value = err.message
  } finally {
    saving.value = false
  }
}

async function toggleTask(task) {
  if (saving.value) return
  saving.value = true
  error.value = ''
  try {
    const updated = await updateTask(task.id, !task.completed)
    task.completed = updated.completed
  } catch (err) {
    error.value = err.message
  } finally {
    saving.value = false
  }
}

async function removeTask(id) {
  if (saving.value) return
  saving.value = true
  error.value = ''
  try {
    await deleteTask(id)
    tasks.value = tasks.value.filter(task => task.id !== id)
  } catch (err) {
    error.value = err.message
  } finally {
    saving.value = false
  }
}

onMounted(loadTasks)
</script>

<template>
  <main class="page">
    <header class="brand">
      <span class="brand-icon" aria-hidden="true">✓</span>
      <span>小步学习</span>
      <span class="brand-note">我的第一个前后端项目</span>
    </header>

    <section class="intro">
      <p class="eyebrow">从一件小事开始</p>
      <h1>今天，学一点。</h1>
      <p class="intro-text">把想学的事写下来，一次完成一小步。</p>
    </section>

    <section class="task-card" aria-labelledby="list-title">
      <div class="card-heading">
        <div>
          <h2 id="list-title">学习任务</h2>
          <p v-if="loading">正在读取任务…</p>
          <p v-else>已完成 {{ completedCount }} / {{ tasks.length }} 项</p>
        </div>
        <span class="heading-badge">慢慢来，也在前进</span>
      </div>

      <div
        class="progress-track"
        role="progressbar"
        aria-label="学习任务完成进度"
        :aria-valuenow="completedCount"
        :aria-valuemax="tasks.length || 1"
        aria-valuemin="0"
      >
        <div class="progress-fill" :style="{ width: `${progress}%` }"></div>
      </div>

      <!-- v-model 把输入框内容和 newTitle 关联；@submit 监听表单提交。 -->
      <form class="add-form" @submit.prevent="addTask">
        <label class="sr-only" for="new-task">新的学习任务</label>
        <input
          id="new-task"
          v-model="newTitle"
          type="text"
          maxlength="80"
          placeholder="接下来，你想学什么？"
          autocomplete="off"
          :disabled="loading || saving"
        />
        <button class="add-button" type="submit" :disabled="loading || saving || !newTitle.trim()">
          <span aria-hidden="true">＋</span> 添加任务
        </button>
      </form>

      <div v-if="error" class="error-message" role="alert">
        <span>{{ error }}</span>
        <button type="button" :disabled="loading || saving" @click="loadTasks">重新读取</button>
      </div>

      <p v-if="loading" class="empty-state" role="status">正在和后端打个招呼…</p>
      <p v-else-if="!tasks.length && !error" class="empty-state">清单还是空的。添加一件想学的小事吧。</p>

      <!-- v-for 遍历列表；:key 用任务 ID 帮助 Vue 识别每一项。 -->
      <ul v-else class="task-list">
        <li v-for="task in tasks" :key="task.id" class="task-row" :class="{ completed: task.completed }">
          <button
            class="check-button"
            type="button"
            role="checkbox"
            :aria-checked="task.completed"
            :aria-label="task.title"
            :disabled="saving || loading"
            @click="toggleTask(task)"
          >
            <span v-if="task.completed" aria-hidden="true">✓</span>
          </button>
          <span class="task-title">{{ task.title }}</span>
          <button
            class="delete-button"
            type="button"
            :aria-label="`删除任务：${task.title}`"
            :disabled="saving || loading"
            @click="removeTask(task.id)"
          >删除</button>
        </li>
      </ul>

      <p class="card-footer">小提示：输入后按 Enter，也可以添加任务。</p>
    </section>

    <footer class="page-footer">
      <p>一次小练习，串起前端与后端。</p>
      <p class="memory-note">任务暂存在后端内存里，重启后端会恢复示例任务。</p>
    </footer>
  </main>
</template>

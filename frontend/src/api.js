// 这个文件只负责 HTTP 请求，页面怎么显示由 App.vue 决定。
// fetch 是浏览器自带的请求工具，这里不需要安装 Axios。
async function request(path, options = {}) {
  let response
  try {
    response = await fetch(`/api${path}`, options)
  } catch {
    throw new Error('请求失败，请检查前后端是否已经启动')
  }

  if (!response.ok) {
    const data = await response.json().catch(() => ({}))
    // FastAPI 的字段校验错误是一个数组，普通业务错误通常是一段文字。
    const message = typeof data.detail === 'string' ? data.detail :
      response.status === 422 ? '任务内容需要是 1～80 个字符' :
      '请求失败，请检查后端是否已经启动，再重试'
    throw new Error(message)
  }

  // 删除接口返回 204，没有 JSON 内容可以读取。
  if (response.status === 204) return
  return response.json()
}

export function getTasks() {
  return request('/tasks')
}

export function createTask(title) {
  return request('/tasks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title }),
  })
}

export function updateTask(id, completed) {
  return request(`/tasks/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ completed }),
  })
}

export function deleteTask(id) {
  return request(`/tasks/${id}`, { method: 'DELETE' })
}

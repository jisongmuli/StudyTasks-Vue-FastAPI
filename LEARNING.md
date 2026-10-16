# 从一点 Java 基础开始，读懂这个项目

不用先记住所有语法。第一轮的目标是：知道文件负责什么，并能追踪“添加任务”这一次操作。

## 第一步：分清前端和后端

前端运行在浏览器里，负责显示任务、读取输入、响应点击。

后端运行在电脑上的 Python 进程里，负责接收请求、校验内容、保存和修改任务。

它们通过 HTTP 请求和 JSON 数据交流。浏览器不能直接读取后端的 Python 列表，必须请求一个接口。

你之前学过 Spring Boot，可以先用下面的对应关系找熟悉感：

| Java / Spring Boot 中见过的概念 | 这个项目里的对应内容 |
| --- | --- |
| Controller 方法 | `main.py` 中的四个接口函数 |
| `@GetMapping` / `@PostMapping` | `@app.get` / `@app.post` |
| DTO、请求对象 | `TaskCreate` 和 `TaskUpdate` |
| 请求体、`@RequestBody` | `body: TaskCreate`，FastAPI 根据模型读取 JSON 请求体 |
| 路径参数、`@PathVariable` | 路径中的 `{task_id}` 和函数里的 `task_id: int` |
| Maven 依赖声明 | 后端 `requirements.txt`；前端 `package.json` 的依赖部分 |
| application.yml 中的端口概念 | 启动命令里的 `--port 8000` |

这些是帮助理解的类比，并不是技术实现完全相同。

**小练习**：分别打开页面和 `/api/tasks`。前者是你操作的界面，后者是原始数据。

## 第二步：知道页面从哪里开始

阅读顺序：`frontend/index.html` → `frontend/src/main.js` → `frontend/src/App.vue`。

1. 浏览器加载 `index.html`。
2. HTML 加载 `main.js`。
3. `main.js` 创建 Vue 应用，把 `App.vue` 放到 `id="app"` 的元素里。

`App.vue` 里有两部分：

- `<script setup>`：JavaScript，保存数据、定义函数。
- `<template>`：页面模板，决定显示什么、点击时调用什么函数。

样式集中在 `style.css`。Vue 也支持把样式写在 `.vue` 文件的 `<style>` 中，本项目单独放置，便于阅读。

**小练习**：把 `App.vue` 中的“今天，学一点。”改成你喜欢的一句话。保存文件后，观察页面变化。

## 第三步：理解 Vue 的“数据驱动页面”

先找这行：

```js
const tasks = ref([])
```

`[]` 是一个空数组。`ref` 让 Vue 跟踪数据变化：当 `tasks` 更新时，依赖它的页面也会更新。

在 JavaScript 代码里，通过 `tasks.value` 访问数组；在模板里，Vue 自动处理这层包装，直接写 `tasks`。

然后在模板里找：

```html
<li v-for="task in tasks" :key="task.id">
```

它的意思是“对数组中的每个任务，都生成一个列表项”。和你见过的 `for` 循环很像。

本项目用到的 Vue 基础语法：

| 语法 | 含义 | 项目中的例子 |
| --- | --- | --- |
| `{{ ... }}` | 显示变量内容 | `{{ task.title }}` |
| `v-model` | 把输入框和变量关联起来 | 输入框关联 `newTitle` |
| `v-for` | 循环显示 | 显示每条任务 |
| `v-if` / `v-else` | 按条件显示 | 加载提示、空列表提示 |
| `@click` | 监听点击 | 点击后调用 `toggleTask` |
| `:disabled` | 用表达式决定 HTML 属性 | 请求期间禁用按钮 |
| `@submit.prevent` | 监听表单提交，阻止浏览器默认刷新 | 调用 `addTask` |
| `computed` | 根据其他数据计算一个值 | 已完成的任务数量 |
| `onMounted` | 页面组件挂载后执行 | 调用 `loadTasks` 读取任务 |

`const` 声明一个不能重新赋值的变量引用，不代表里面的数组不能修改。`tasks.value.push(task)` 仍然可以添加一项。

**小练习**：勾选一个任务，观察文字、完成数量和进度条一起变化。找到 `completedCount` 的计算代码。

## 第四步：跟着一次“添加任务”走

按顺序找到这些位置：

1. `App.vue` 的输入框：`v-model="newTitle"` 把输入写入变量。
2. 表单：`@submit.prevent="addTask"` 触发函数。
3. `addTask()`：读取输入，调用 `createTask(title)`。
4. `api.js` 的 `createTask()`：把标题变成 JSON，并发出 POST 请求。
5. `vite.config.js` 的 `proxy`：把 `/api` 开头的请求转发到后端。
6. `main.py` 的 `create_task()`：接收请求，生成 ID，保存任务。
7. 后端返回新任务，前端执行 `tasks.value.push(task)`，页面出现新的一行。

特别注意：**前端先等后端返回，再更新页面列表**。这样能确认任务已经被后端接受。

看懂这几个 JavaScript 词就够了：

- `import` / `export`：从其他文件导入内容、把内容提供给其他文件使用。
- `async` / `await`：请求需要时间；`await` 等结果回来，再继续这个函数后面的步骤。
- `fetch`：浏览器提供的 HTTP 请求工具。
- `JSON.stringify(...)`：把 JavaScript 对象转成 JSON 字符串，作为请求体发送。
- `response.json()`：把响应中的 JSON 解析成 JavaScript 数据。
- `try` / `catch` / `finally`：成功时继续处理，失败时显示错误，最后解除按钮禁用状态。

**小练习**：打开浏览器开发者工具（一般是 F12），切到 Network / 网络，添加任务。找到 `POST /api/tasks`，查看请求体和响应。浏览器里看到的请求端口是 5173，因为它先经过 Vite 转发。

## 第五步：读懂后端最关键的三件事

先读 `backend/main.py` 的 `TaskCreate`：

```python
class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=80)
```

意思是“创建任务时，必须提供字符串标题，长度为 1～80”。类可以类比 Java 的类，`title: str` 是类型标注。Pydantic 用模型校验请求；后面的校验函数还会去掉首尾空格，并拒绝纯空格标题。

再找接口：

```python
@app.post("/api/tasks", response_model=Task, status_code=201)
async def create_task(body: TaskCreate):
```

- `@app.post`：这个函数处理 POST 请求。
- `/api/tasks`：请求的路径。
- `body: TaskCreate`：用这个模型解析和校验请求体。
- `response_model=Task`：约定响应的任务数据结构。
- `201`：表示创建成功。
- `async def`：定义异步函数。本项目的内存操作很短，先理解接口映射即可。

最后找 `tasks.append(task)` 和 `return task`：一个保存数据，一个把数据返回给前端。FastAPI 会把模型转换成 JSON 响应。

常见状态码：

| 状态码 | 本项目中的意思 |
| --- | --- |
| 200 | 读取或修改成功 |
| 201 | 创建成功 |
| 204 | 删除成功，没有响应体 |
| 404 | 指定任务不存在 |
| 422 | 请求格式或字段内容不符合模型要求 |

**小练习**：打开 `http://127.0.0.1:8000/docs`，展开 GET 接口，点 `Try it out` → `Execute`。再尝试 POST，填入 `{"title":"从接口文档添加任务"}`。回到页面刷新，确认新任务出现。

## 第一轮学完的判断标准

你能回答下面几个问题，就已经看懂这个项目的主干了：

1. 改页面标题应该去哪个文件？
2. 添加任务的点击事件在哪里处理？
3. 前端在哪个文件发请求？
4. 后端怎么知道该执行哪个函数？
5. 任务保存在哪里？为什么重启后端会重置？
6. `package.json` 和 `requirements.txt` 分别负责什么？

答案：`App.vue`；`App.vue` 的 `addTask`；`api.js`；HTTP 方法与路径匹配接口装饰器；`main.py` 的内存列表；分别声明前端和后端依赖（`package.json` 还定义运行命令）。

下一轮可以先加“任务备注”，练习同时改前端输入、请求内容和后端模型；读懂后再加入 SQLite 保存数据。一次只扩展一个概念。

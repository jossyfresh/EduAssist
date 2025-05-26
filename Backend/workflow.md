# Learning Path Workflow

## 1. Generate Learning Path Outline

- **Endpoint:** `GET /api/v1/learning-paths/course/{course_id}/outline`
- **Description:** Get or generate a learning path outline for a course
- **Response:** Outline with chapters and estimated durations

## 2. Create Learning Path

- **Endpoint:** `POST /api/v1/learning-paths/course/{course_id}/create-from-outline`
- **Description:** Create a learning path from the generated outline
- **Response:** Created learning path with steps

## 3. Get Learning Path Steps

- **Endpoint:** `GET /api/v1/learning-paths/course/{course_id}/steps`
- **Description:** Get all steps for a learning path
- **Response:** List of steps with their IDs, titles, and descriptions

## 4. Track Progress

- **Endpoint:** `POST /api/v1/learning-paths/progress/{path_id}/step/{step_id}`
- **Description:** Mark a step as completed
- **Request Body:** `{ "completed": true }`
- **Response:** Updated progress entry

## 5. View Progress

- **Endpoint:** `GET /api/v1/learning-paths/progress/{path_id}`
- **Description:** Get all progress entries for a learning path
- **Response:** List of completed steps with completion timestamps

## Example Flow

1. Get outline for course
2. Create learning path from outline
3. Get steps to see what needs to be completed
4. As user completes steps, mark them as completed
5. Track overall progress through the learning path

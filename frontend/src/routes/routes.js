import MainLayout from "@/pages/Layout/MainLayout.vue";
import SpeedOptView from "@/pages/SpeedOptView.vue";
import TugConfigView from "@/pages/TugConfigView.vue";
import TaskView from "@/pages/TaskView.vue";
import TaskConfigView from "@/pages/TaskConfigView.vue";
import AboutView from "@/pages/AboutView.vue";

const routes = [
  {
    path: "/",
    component: MainLayout,
    redirect: "/speed-opt",
    children: [
      {
        path: "speed-opt",
        name: "Speed optimization",
        component: SpeedOptView
      },
      {
        path: "tug-config",
        name: "Tug Config",
        component: TugConfigView
      },
      {
        path: "task-status",
        name: "TaskView",
        component: TaskView
      },
      {
        path: "task-config",
        name: "Task Config",
        component: TaskConfigView
      },
      {
        path: "about",
        name: "About us",
        component: AboutView
      }
    ]
  }
];

export default routes;

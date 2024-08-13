import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import FeedView from '@/views/FeedView.vue'
import ChatView from '@/views/ChatView.vue'
import NotificationsView from '@/views/NotificationsView.vue'
import SearchView from '@/views/SearchView.vue'
import ProfileView from '@/views/ProfileView.vue'
import PostView from '@/views/PostView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      children: [
        { path: '/', name: 'feed', component: FeedView },
        { path: '/chat', name: 'chat', component: ChatView },
        { path: '/notifications', name: 'notifications', component: NotificationsView },
        { path: '/search', name: 'search', component: SearchView },
        { path: '/user/:id', name: 'profile', component: ProfileView },
        { path: '/post/:id', name: 'post', component: PostView },
      ]
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('../views/SignupView.vue')
    },
  ],
  scrollBehavior(to, from, savedPosition) {
    return { top: 0 }
  }
})

export default router

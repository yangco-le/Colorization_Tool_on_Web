import Vue from 'vue'
import Router from 'vue-router'
import ColorizationPage from '@/components/ColorizationPage'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'ColorizationPage',
      component: ColorizationPage
    }
  ]
})

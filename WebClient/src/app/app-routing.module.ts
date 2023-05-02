import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ClothesPreviewComponent } from 'src/app/pages/clothes-preview/clothes-preview.component';
import { AuthGuard } from './authService/auth-guard';
import { AddClothesComponent } from './pages/add-clothes/add-clothes.component';
import { CreateSetComponent } from './pages/create-set/create-set.component';
import { HomeComponent } from './pages/home/home.component';
import { LoginComponent } from './pages/login/login.component';
import { PreviewSetsComponent } from './pages/preview-sets/preview-sets.component';
import { SettingsComponent } from './pages/settings/settings.component';
import { SignUpComponent } from './pages/sign-up/sign-up.component';
import { WardrobeConnectionComponent } from './pages/wardrobe-connection/wardrobe-connection.component';
import { ManualCreateSetComponent } from './pages/manual-create-set/manual-create-set.component';


const routes: Routes = [
  { path: 'sign-up', component: SignUpComponent },
  { path: 'login', component: LoginComponent },
  { path: '', component: HomeComponent, canActivate: [AuthGuard] },
  { path: 'add-clothes', component: AddClothesComponent, canActivate: [AuthGuard] },
  { path: 'clothes-preview', component: ClothesPreviewComponent, canActivate: [AuthGuard] },
  { path: 'create-set', component: CreateSetComponent, canActivate: [AuthGuard] },
  { path: 'preview-sets', component:PreviewSetsComponent, canActivate: [AuthGuard] },
  { path: 'wardrobe-connection', component: WardrobeConnectionComponent, canActivate: [AuthGuard] },
  { path: 'settings', component: SettingsComponent, canActivate: [AuthGuard] },
  { path: 'manual-create-set', component: ManualCreateSetComponent, canActivate: [AuthGuard] },

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {

}

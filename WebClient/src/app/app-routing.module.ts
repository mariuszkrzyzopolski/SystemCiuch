import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ClothesPreviewComponent } from 'src/app/pages/clothes-preview/clothes-preview.component';
import { AddClothesComponent } from './pages/add-clothes/add-clothes.component';
import { CreateSetComponent } from './pages/create-set/create-set.component';
import { HomeComponent } from './pages/home/home.component';
import { LoginComponent } from './pages/login/login.component';
import { PreviewSetsComponent } from './pages/preview-sets/preview-sets.component';
import { SettingsComponent } from './pages/settings/settings.component';
import { SignUpComponent } from './pages/sign-up/sign-up.component';
import { WardrobeConnectionComponent } from './pages/wardrobe-connection/wardrobe-connection.component';


const routes: Routes = [
  {path:'sign-up', component:SignUpComponent},
  {path:'login', component:LoginComponent},
  { path: '', component: HomeComponent },
  {path: 'add-clothes', component:AddClothesComponent },
  { path: 'clothes-preview', component: ClothesPreviewComponent },
  { path: 'create-set', component: CreateSetComponent},
  { path: 'preview-sets', component: PreviewSetsComponent},
  { path: 'wardrobe-connection', component: WardrobeConnectionComponent  },
  { path: 'settings', component: SettingsComponent },
 
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
  
 }

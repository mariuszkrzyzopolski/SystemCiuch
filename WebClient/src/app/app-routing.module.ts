import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CollectionPreviewComponent } from 'src/app/pages/collection-preview/collection-preview.component';
import { AddToCollectionComponent } from './pages/add-to-collection/add-to-collection.component';
import { CollectionSelectionComponent } from './pages/collection-selection/collection-selection.component';
import { HelpComponentComponent } from './pages/help-component/help-component.component';
import { HomeComponent } from './pages/home/home.component';
import { SettingsComponent } from './pages/settings/settings.component';
import { WardrobeConnectionComponent } from './pages/wardrobe-connection/wardrobe-connection.component';


const routes: Routes = [
  { path: '', component: HomeComponent },
  {path: 'add-to-collection', component:AddToCollectionComponent },
  { path: 'collection-preview', component: CollectionPreviewComponent },
  { path: 'collection-selection', component: CollectionSelectionComponent},
  { path: 'wardrobe-connection', component: WardrobeConnectionComponent  },
  { path: 'settings', component: SettingsComponent },
  { path: 'help-component', component: HelpComponentComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
  
 }

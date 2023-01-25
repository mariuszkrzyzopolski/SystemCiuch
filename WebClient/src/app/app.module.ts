import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';
import { HeaderComponent } from './header/header.component';
import { MenuChoiceComponent } from './menu-choice/menu-choice.component';
import { FooterComponent } from './footer/footer.component';
import { CollectionPreviewComponent } from 'src/app/pages/collection-preview/collection-preview.component';
import { AppRoutingModule } from './app-routing.module';
import { HomeComponent } from './pages/home/home.component';
import { AddToCollectionComponent } from './pages/add-to-collection/add-to-collection.component';
import { SettingsComponent } from './pages/settings/settings.component';
import { WardrobeConnectionComponent } from './pages/wardrobe-connection/wardrobe-connection.component';
import { HelpComponentComponent } from './pages/help-component/help-component.component';
import { CollectionSelectionComponent } from './pages/collection-selection/collection-selection.component';


@NgModule({
  declarations: [
    AppComponent,
    MenuChoiceComponent,
    HeaderComponent,
    FooterComponent,
    CollectionPreviewComponent,
    HomeComponent,
    AddToCollectionComponent,
    CollectionSelectionComponent,
    WardrobeConnectionComponent,
    SettingsComponent,
    HelpComponentComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule  
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

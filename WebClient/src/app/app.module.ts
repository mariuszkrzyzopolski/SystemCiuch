import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';
import { HeaderComponent } from './header/header.component';
import { MenuChoiceComponent } from './menu-choice/menu-choice.component';
import { FooterComponent } from './footer/footer.component';
import { ClothesPreviewComponent } from 'src/app/pages/clothes-preview/clothes-preview.component';
import { AppRoutingModule } from './app-routing.module';
import { HomeComponent } from './pages/home/home.component';
import { AddClothesComponent } from './pages/add-clothes/add-clothes.component';
import { SettingsComponent } from './pages/settings/settings.component';
import { WardrobeConnectionComponent } from './pages/wardrobe-connection/wardrobe-connection.component';
import { CreateSetComponent } from './pages/create-set/create-set.component';
import { PreviewSetsComponent } from './pages/preview-sets/preview-sets.component';
import { SwiperModule } from "swiper/angular";
import { FormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    AppComponent,
    MenuChoiceComponent,
    HeaderComponent,
    FooterComponent,
    ClothesPreviewComponent,
    HomeComponent,
    AddClothesComponent,
    CreateSetComponent,
    WardrobeConnectionComponent,
    SettingsComponent,
    PreviewSetsComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    SwiperModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

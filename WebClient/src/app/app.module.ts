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
import { ReactiveFormsModule } from '@angular/forms';
import {HttpClientModule, HTTP_INTERCEPTORS} from '@angular/common/http';
import { SignUpComponent } from './pages/sign-up/sign-up.component';
import { LoginComponent } from './pages/login/login.component';
import { AuthInterceptor } from './auth-interceptor/auth-interceptor';
import { AuthGuard } from './authService/auth-guard';
import { SliderComponent } from './slider/slider.component';

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
    SignUpComponent,
    LoginComponent,
    SliderComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    SwiperModule,
    ReactiveFormsModule,
    HttpClientModule,
  ],
  providers: [{
    provide: HTTP_INTERCEPTORS,
    useClass: AuthInterceptor,
    multi: true,
  },
    AuthGuard],
  bootstrap: [AppComponent]
})
export class AppModule { }

import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'wardrobe-app';
}

export const env = {
  url: 'http://0.0.0.0:8000',
};

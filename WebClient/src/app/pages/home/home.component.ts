import { Component } from '@angular/core';
import { MenuItem } from '../../model/MenuItem';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  
  public MenuItems: Array<MenuItem> = [
    { name: 'Dodaj ubranie', route: '/add-clothes' },
    { name: 'Podgląd ubrań', route: '/clothes-preview' },
    { name: 'Tworzenie zestawu', route: '/create-set' },
    { name: 'Podgląd zestawów', route: '/prewiew-sets' },
    { name: 'Połącz z szafą', route:'/wardrobe-connection'},
    { name: 'Ustawienia', route: '/settings' }]
    
}

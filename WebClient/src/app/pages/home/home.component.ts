import { Component } from '@angular/core';
import { MenuItem } from '../../model/MenuItem';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  
  public MenuItems: Array<MenuItem> = [
    { name: 'Dodawanie do kolekcji', route: '/add-to-collection' },
    { name: 'Podgląd kolekcji', route: '/collection-preview' },
    { name: 'Dobór kolekcji', route: '/collection-selection' },
    { name: 'Połącz z szafą', route:'/wardrobe-connection'},
    { name: 'Ustawienia', route: '/settings' },
    { name: 'Pomoc', route: '/help-component' }]

}

import { Component, Input } from '@angular/core';
import { Collection } from 'src/app/model/Collection';

@Component({
  selector: 'app-clothes-prviev',
  templateUrl: './clothes-preview.component.html',
  styleUrls: ['./clothes-preview.component.css']
})
export class ClothesPreviewComponent {
  public collections: Array<Collection> = [
    { name: 'Kolekcja 1', route: './collection1' },
    { name: 'Kolekcja 2', route: './collection2' },
    { name: 'Kolekcja 3', route: './collection3' },
    { name: 'Kolekcja 4', route: './collection4'},
    { name: 'Kolekcja 5', route: './collection5' },
    { name: 'Wszystkie', route: './all' },
  ] 
}

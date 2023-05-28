import { Component } from '@angular/core';
import { CollectionService } from '../services/CollectionService';
import { Router } from '@angular/router';

@Component({
  selector: 'app-automatic-create-set',
  templateUrl: './automatic-create-set.component.html',
  styleUrls: ['./automatic-create-set.component.css']
})
export class AutomaticCreateSetComponent {
  constructor(private collectionService: CollectionService, private router: Router) { }
  
  createSet(category: string) {
    this.collectionService.saveAutomaticSet(category).subscribe(response => {
      this.router.navigate([ '/preview-sets' ]);
    })
  }
}

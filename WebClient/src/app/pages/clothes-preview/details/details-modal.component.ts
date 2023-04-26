import { Component, Input } from '@angular/core';
import { DTOCollectionItemDetails } from 'src/app/model/CollectionDTO';

@Component({
  selector: 'app-details-modal',
  templateUrl: './details-modal.component.html'
})
export class DetailsModalComponent {
  @Input() item: DTOCollectionItemDetails | null;
}
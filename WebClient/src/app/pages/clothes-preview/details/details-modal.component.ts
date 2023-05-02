import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ItemTags } from 'src/app/model/ItemTags';
import { DTOCollectionItemDetails } from 'src/app/model/DTOCollection';

@Component({
  selector: 'app-details-modal',
  templateUrl: './details-modal.component.html'
})
export class DetailsModalComponent implements OnInit {
  constructor(private formBuilder: FormBuilder) { }
  
  ngOnInit(): void {
    this.tagsForm = this.formBuilder.group({
      tags: ['', Validators.required]
    });
  }
  @Input() visible: boolean = false;

  @Input() set item(i:  DTOCollectionItemDetails | null) {
    this._item = i;
    let form = this.tagsForm;
    if(form) {
      this.tagsForm.get("tags")?.setValue(i?.tags);
    }
  }

  _item: DTOCollectionItemDetails | null;
  get itemDetails(): DTOCollectionItemDetails | null {
      return this._item;
  }

  @Input() edit: boolean = false;

  @Output() cancelEvent = new EventEmitter<void>();
  @Output() saveEvent = new EventEmitter<ItemTags>();
  tagsForm: FormGroup;

  onCancel(){
    this.cancelEvent.emit();
  }

  onSubmit() {
    var values = this.tagsForm.value
    this.saveEvent.emit({id: this.itemDetails!.id, tags: values.tags.split(',')} as ItemTags);
  }
}
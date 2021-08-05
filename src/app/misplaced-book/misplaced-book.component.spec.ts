import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MisplacedBookComponent } from './misplaced-book.component';

describe('MisplacedBookComponent', () => {
  let component: MisplacedBookComponent;
  let fixture: ComponentFixture<MisplacedBookComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MisplacedBookComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MisplacedBookComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

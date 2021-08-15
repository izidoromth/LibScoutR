import { Injector, NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SearchBookComponent } from './components/search-book/search-book.component';
import { MisplacedBookComponent } from './components/misplaced-book/misplaced-book.component';
import { LibrarianLoginComponent } from './components/librarian-login/librarian-login.component';
import { MaterialComponentsModule } from './components/material-components/material-components.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatSpinnerOverlayComponent } from './components/mat-spinner-overlay/mat-spinner-overlay.component';


@NgModule({
  declarations: [
    AppComponent,
    SearchBookComponent,
    MisplacedBookComponent,
    LibrarianLoginComponent,
    MatSpinnerOverlayComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MaterialComponentsModule,
    BrowserAnimationsModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
  static injector: Injector;
  constructor(injector: Injector) {
    AppModule.injector = injector;
  }
}

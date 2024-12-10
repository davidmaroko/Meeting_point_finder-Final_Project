import React from 'react';
import Navbar from "../parts/Navbar";
import David from '../../img/anonymous.jpg';
import Anonymous from '../../img/anonymous.jpg';
import FooterComponent from "../parts/FooterComponent";
const AboutPage = () => {
  return (
      <>
          <Navbar/>
          <div className={"container mt-5"}>
              <div className="row justify-content-evenly">
                  <figure className="col-auto">
                      <img src={David} className="rounded-circle" alt="David"/>
                      <figcaption className={"text-secondary"}>David Maroko</figcaption>
                  </figure>
                  <figure className="col-auto">
                      <img src={Anonymous} className="rounded-circle" alt="Anonymous"/>
                      <figcaption className={"text-secondary"}>Mendel Bismut</figcaption>
                  </figure>
              </div>
              <div className={"row  my-5 shadow-lg p-3 mb-5 bg-body rounded"}>
                  <div className={"col-md-6 m-auto"}>
                              <h1 className={"border-bottom border-warning pb-2"}>מטרת הפרויקט</h1>
        <p>
פלטפורמה מקוונת
המאפשרת למטיילים דתיים
ליצור ולהשתתף במניין
באזורים בהם אין בתי כנסת</p>
        <h1 className={"border-bottom border-warning pb-2"}>מורכבות הפרויקט</h1>
        <p>על מנת למצוא את המיקום הכי קרוב לכל
המשתתפים במניין, על המערכת לזהות תחילה
את האנשים המתאימים ולחשב את הנקודה
המרכזית ביניהם, דהיינו הנקודה שהסכום הכולל
של מרחקי הנסיעה ממנה אל עבר המתפללים
הוא הקצר ביותר. תהליך זה מורכב ומצריך
חישובים מרובים וארוכים. עיבוד מהיר וקיצור
הזמן של שני התהליכים הם אתגרים מורכבים
מתחום מדעי המחשב</p>
        <h1 className={"border-bottom border-warning pb-2"}>הפתרון שלנו</h1>
        <p>המערכת מחלקת את המתפללים ברחבי העולם
לקבוצות של מתפללים קרובים. לכל קבוצה, נוצרת
מפה הכוללת את מיקומיהם, ומיוצגת כגרף - רשת
של קווים ונקודות. ואז מתבצע חיפוש אחר הנקודה
המרכזית בגרף. על מנת לחסוך בזמן, אנו מחפשים
תחילה אזור אופטימלי בגרף על ידי בדיקת מדגם
מייצג של נקודות, ואז מבצעים חיפוש מפורט רק
באותו אזור כדי למצוא את הנקודה המדויקת.</p>
                  </div>
              </div>

    </div>
          <FooterComponent/>
      </>

  );
};

export default AboutPage;

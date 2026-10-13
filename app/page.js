import Link from "next/link";
import { integrantes, actividades } from "@/data/actividades";

export default function Home() {
  return (
    <>
      <section className="hero">
        <p className="eyebrow">Taller 4 · Actividades 1 a 8 · AWS</p>
        <h1 className="title">
          Arquitectura AWS segura,
          <br />
          <span className="grad">disponible y escalable</span>
        </h1>
        <p className="hero-sub">
          Cada integrante presenta sus actividades en la consola de AWS.
        </p>
        <Link href="/actividades/1" className="btn-pink">
          Comenzar <span className="mi">arrow_forward</span>
        </Link>
      </section>

      <section className="tiles">
        <div className="tile tile-pink">
          <div>
            <div className="tile-label">El equipo presenta</div>
            <div className="mission">
              Ocho actividades para construir una nube segura, fiable y
              escalable
            </div>
          </div>
          <div className="stats">
            <div>
              <span>Actividades</span>
              <strong>8</strong>
            </div>
            <div>
              <span>Integrantes</span>
              <strong>4</strong>
            </div>
            <div>
              <span>Servicios AWS</span>
              <strong>6</strong>
            </div>
          </div>
        </div>

        {actividades.map((a) => (
          <Link key={a.id} href={`/actividades/${a.id}`} className="tile">
            <div>
              <div className="tile-label">Actividad {a.id}</div>
              <h3>{a.titulo}</h3>
              <div className="tile-sub">{a.integrante}</div>
            </div>
            <span className="circle">
              <span className="mi">arrow_forward</span>
            </span>
          </Link>
        ))}
      </section>

      <section className="section" style={{ marginTop: 72 }}>
        <h2>
          Un vistazo por <span className="grad">integrante</span>
        </h2>
        <div className="members">
          {integrantes.map((it) => (
            <div className="member" key={it.n}>
              <div className="num">0{it.n}</div>
              <h3>{it.nombre}</h3>
              {it.act.map((id) => {
                const a = actividades.find((x) => x.id === id);
                return (
                  <Link key={id} href={`/actividades/${id}`}>
                    <span>Act {id}</span> {a.titulo}
                  </Link>
                );
              })}
            </div>
          ))}
        </div>
      </section>

      <section className="statement">
        <h2>
          Una arquitectura <span className="grad">disponible</span>,
          monitoreada y optimizada
        </h2>
        <Link href="/actividades/4" className="btn-white">
          Ver la demo del ALB <span className="mi">arrow_forward</span>
        </Link>
      </section>
    </>
  );
}

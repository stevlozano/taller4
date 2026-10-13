import Link from "next/link";
import { notFound } from "next/navigation";
import { actividades } from "@/data/actividades";
import { DataTable } from "@/components/DataTable";
import Figures from "@/components/Figures";

export function generateStaticParams() {
  return actividades.map((a) => ({ id: String(a.id) }));
}

export async function generateMetadata({ params }) {
  const { id } = await params;
  const a = actividades.find((x) => x.id === Number(id));
  return { title: a ? `Act ${a.id} · ${a.titulo} — Taller 4 AWS` : "Taller 4 AWS" };
}

function Table({ data }) {
  return <DataTable data={data} label="Datos de la actividad" />;
}

export default async function Actividad({ params }) {
  const { id: idStr } = await params;
  const id = Number(idStr);
  const a = actividades.find((x) => x.id === id);
  if (!a) notFound();

  const prev = actividades.find((x) => x.id === id - 1);
  const next = actividades.find((x) => x.id === id + 1);

  return (
    <article>
      <header className="act-head">
        <p className="eyebrow">
          Actividad {a.id} · {a.area} · {a.integrante}
        </p>
        <h1 className="title">
          {a.titulo.includes(":") ? (
            <>
              {a.titulo.split(":")[0]}:{" "}
              <span className="grad">{a.titulo.split(":").slice(1).join(":").trim()}</span>
            </>
          ) : (
            a.titulo
          )}
        </h1>
        <div className="objetivo">{a.objetivo}</div>
        {a.intro && <p className="act-intro">{a.intro}</p>}
      </header>

      {a.img && <Figures images={a.img} />}

      {a.pilares && (
        <section className="section">
          <h2 className="eb">Los seis pilares</h2>
          <div className="pillars">
            {a.pilares.map(([name, desc, explain]) => (
              <div className="pillar" key={name}>
                <strong>{name}</strong>
                <span>{desc}</span>
                {explain && <p className="pillar-more">{explain}</p>}
              </div>
            ))}
          </div>
        </section>
      )}

      {a.pasos && (
        <section className="section">
          <h2 className="eb">{a.tituloPasos || "Procedimiento"}</h2>
          <ol className="steps">
            {a.pasos.map((p, i) => (
              <li key={i}>{p}</li>
            ))}
          </ol>
        </section>
      )}

      {a.codigo && (
        <section className="section">
          <h2 className="eb">Script de User data</h2>
          <pre>{a.codigo}</pre>
        </section>
      )}

      {a.puntos && (
        <section className="section">
          <h2 className="eb">{a.tituloPuntos || "Verificación"}</h2>
          <ul className="bullets">
            {a.puntos.map((p, i) => (
              <li key={i}>{p}</li>
            ))}
          </ul>
        </section>
      )}

      {a.puntos2 && (
        <section className="section">
          <h2 className="eb">{a.tituloPuntos2}</h2>
          <ul className="bullets">
            {a.puntos2.map((p, i) => (
              <li key={i}>{p}</li>
            ))}
          </ul>
        </section>
      )}

      {a.puntos3 && (
        <section className="section">
          <h2 className="eb">{a.tituloPuntos3}</h2>
          <ul className="bullets">
            {a.puntos3.map((p, i) => (
              <li key={i}>{p}</li>
            ))}
          </ul>
        </section>
      )}

      {a.analogia && (
        <section className="section">
          <div className="note">{a.analogia}</div>
        </section>
      )}

      {a.tabla && (
        <section className="section">
          <h2 className="eb">{a.tablaTitulo || "Detalle"}</h2>
          <Table data={a.tabla} />
        </section>
      )}

      {a.tabla2 && (
        <section className="section">
          <h2 className="eb">{a.tituloTabla2}</h2>
          <Table data={a.tabla2} />
        </section>
      )}

      {a.demo && (
        <section className="section">
          <h2 className="eb">Demostración: cambiar el título en cada servidor</h2>
          <pre>{a.demo.join("\n")}</pre>
        </section>
      )}

      {a.preguntaResp && a.pregunta && (
        <section className="section">
          <h2 className="eb">{a.pregunta}</h2>
          <div className="note">{a.preguntaResp}</div>
        </section>
      )}

      {a.pregunta && !a.preguntaResp && (
        <section className="section">
          <div className="question">{a.pregunta}</div>
        </section>
      )}

      {a.nota && (
        <section className="section">
          <div className="note">{a.nota}</div>
        </section>
      )}

      {a.cierre && (
        <section className="section">
          <div className="note">{a.cierre}</div>
        </section>
      )}

      <nav className="pager">
        {prev ? (
          <Link href={`/actividades/${prev.id}`}>
            <span className="mi">arrow_back</span> Actividad {prev.id}:{" "}
            {prev.titulo}
          </Link>
        ) : (
          <Link href="/">
            <span className="mi">arrow_back</span> Inicio
          </Link>
        )}
        {next && (
          <Link className="right" href={`/actividades/${next.id}`}>
            Actividad {next.id}: {next.titulo}{" "}
            <span className="mi">arrow_forward</span>
          </Link>
        )}
      </nav>
    </article>
  );
}
